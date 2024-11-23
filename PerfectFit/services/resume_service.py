from celery.exceptions import NotRegistered
from flask import request
from kombu.exceptions import OperationalError
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from config.config_mysql import get_session
from domain.models import Job, AppUser, ProjectExperience, Resume, ProsCons, ResumeSection, Keyword, ResumeView, \
    ResumeLike, Occupation
from dto.resume.resume import ResumeDto
from dto.resume.resume_gpt import ResumeGPT
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from utils.jwt_factory import JWTFactory
from tasks import add_resume_task
from utils.openai.resume.parital_resume_strategy import PartialResumeStrategy
from utils.openai.resume.resume_helper import ResumeHelper

logger = Logger(__name__)


class ResumeService:
    @staticmethod
    def get_resumes(**kwargs):
        with (get_session() as session):
            page = kwargs.get('page', 1)
            count = kwargs.get('count', 10)
            job_id = kwargs.get('job_id')
            occupation_id = kwargs.get('occupation_id')
            level = kwargs.get('level')
            search = kwargs.get('search')

            subquery_count_resume_view = (
                select(func.count(ResumeView.view_id))
                .where(ResumeView.resume_id == Resume.resume_id)
                .scalar_subquery()
            )

            subquery_count_resume_like = (
                select(func.count(ResumeLike.like_id))
                .where(ResumeLike.resume_id == Resume.resume_id)
                .scalar_subquery()
            )

            search_where_clause = Resume.title.like(f"%{search}%") if search else True
            level_where_clause = Resume.level == level if level else True
            job_where_clause = Job.job_id == job_id if job_id else True
            occupation_where_clause = Occupation.occupation_id == occupation_id if occupation_id else True

            order_by_value = [subquery_count_resume_view.desc(), Resume.created_time.desc()] \
                                if kwargs.get('sort') == 'f' else [Resume.created_time.desc()]

            query = (
                select(
                    Resume.resume_id.label('resumeId'),
                    Resume.title,
                    Resume.level,
                    Resume.created_time.label('createdTime'),
                    subquery_count_resume_like.label('likeCount'),
                    subquery_count_resume_view.label('viewCount'),
                    AppUser.username.label('username'),
                    AppUser.profile_path.label('profilePath'),
                    Job.job_name.label('jobName'),
                    Occupation.occupation_name.label('occupationName'),
                )
                .join(AppUser, AppUser.user_id == Resume.user_id)
                .join(Job, Job.job_id == Resume.job_id)
                .join(Occupation, Occupation.occupation_id == Job.occupation_id)
                .filter(
                    Resume.is_shared.is_(True),
                    search_where_clause,
                    level_where_clause,
                    job_where_clause,
                    occupation_where_clause
                )
                .order_by(*order_by_value)
                .offset((page - 1) * count)
                .limit(count)
            )

            total_query = (
                select(func.count(Resume.resume_id))
                .join(AppUser, AppUser.user_id == Resume.user_id)
                .join(Job, Job.job_id == Resume.job_id)
                .join(Occupation, Occupation.occupation_id == Job.occupation_id)
                .filter(
                    Resume.is_shared.is_(True),
                    search_where_clause,
                    level_where_clause,
                    job_where_clause,
                    occupation_where_clause
                )
            )

            resumes = session.execute(query).mappings().all()
            total = session.execute(total_query).scalar()

            return resumes, total

    @staticmethod
    def get_resume_write_data(task_data: ResumeGPT.Response.FullResume.Resume = None):
        with get_session() as session:
            selected_job_query = (
                select(
                    Job.occupation_id
                )
                .where(Job.job_id == task_data.job_id)
                .scalar_subquery()
            )

            job_query = (
                select(
                    Job.job_id.label('jobId'),
                    Job.job_name.label('jobName'),
                    (
                        Job.job_id == task_data.job_id
                    ).label('isSelected')
                )
                .where(
                    Job.occupation_id == selected_job_query
                )
            )

            occupation_query = (
                select(
                    Occupation.occupation_id.label('occupationId'),
                    Occupation.occupation_name.label('occupationName'),
                    (
                        Occupation.occupation_id == selected_job_query
                    ).label('isSelected')
                )
            )

            jobs = session.execute(job_query).mappings().all()
            occupations = session.execute(occupation_query).mappings().all()

            return jobs, occupations

    @staticmethod
    def get_occupations():
        with get_session() as session:
            query = (
                select(
                    Occupation.occupation_id.label('occupationId'),
                    Occupation.occupation_name.label('occupationName')
                )
            )

            occupations = session.execute(query).mappings().all()

            return occupations

    @staticmethod
    def add_resume(request_resume: ResumeDto.Request.Create):
        with get_session() as session:
            user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

            job = session.query(Job).filter(Job.job_id == request_resume.job_id).first()
            if not job:
                raise CustomException(ExceptionType.INVALID_JOB_ID)

            resume = Resume(
                user_id=user_id,
                job_id=request_resume.job_id,
                title=request_resume.title,
                level=request_resume.level,
                is_shared=request_resume.is_shared,
                directional=request_resume.directional if request_resume.directional else None,
            )

            session.add(resume)
            session.flush()

            pros = ProsCons(
                resume_id=resume.resume_id,
                type='장점',
                content=request_resume.pros,
            )

            cons = ProsCons(
                resume_id=resume.resume_id,
                type='단점',
                content=request_resume.cons,
            )

            session.add_all([pros, cons])

            sections = []
            for section in request_resume.sections:
                if not section.title.strip() or not section.content.strip():
                    continue

                resume_section = ResumeSection(
                    resume_id=resume.resume_id,
                    title=section.title,
                    content=section.content,
                )

                sections.append(resume_section)

            session.add_all(sections)

            keywords = []
            for keyword in request_resume.keywords:
                if not keyword.strip():
                    continue

                keyword = Keyword(
                    resume_id=resume.resume_id,
                    job_id=request_resume.job_id,
                    content=keyword,
                )

                keywords.append(keyword)

            session.add_all(keywords)
            session.commit()

    @staticmethod
    def add_section(resume: ResumeDto.Request.CreateFullResume):
        jwt_factory = JWTFactory()
        user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

        if not user_id:
            raise CustomException(ExceptionType.INVALID_TOKEN)

        job = get_session().query(Job).filter(Job.job_id == resume.job_id).first()

        if not job:
            raise CustomException(ExceptionType.INVALID_JOB_ID)

        user: AppUser = (
            get_session()
            .query(AppUser)
            .options(
                joinedload(AppUser.work_experiences),
                joinedload(AppUser.project_experiences)
                .joinedload(ProjectExperience.tasks)
            )
            .filter(AppUser.user_id == user_id)
            .first()
        )

        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        try:
            task = add_resume_task.apply_async(kwargs={
                "job": job,
                "user": user,
                "resume": resume
            })

            return task
        except (TypeError, OperationalError, NotRegistered) as e:
            logger.error("Celery 실행 도중 에러가 발생하였습니다.", e)
            raise CustomException(ExceptionType.CELERY_ERROR)

    @staticmethod
    def add_section_content(dto: ResumeDto.Request.CreateSectionContent):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))
        if not user_id:
            raise CustomException(ExceptionType.INVALID_TOKEN)

        user: AppUser = (
            get_session()
            .query(AppUser)
            .options(
                joinedload(AppUser.work_experiences),
                joinedload(AppUser.project_experiences)
                .joinedload(ProjectExperience.tasks)
            )
            .filter(AppUser.user_id == user_id)
            .first()
        )
        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        job = get_session().query(Job).filter(Job.job_id == dto.job_id).first()
        if not job:
            raise CustomException(ExceptionType.INVALID_JOB_ID)

        resume_helper = ResumeHelper(strategy=PartialResumeStrategy(resume=ResumeGPT.Request.PartialResume.Create(
            keywords=dto.keywords,
            job_name=job.job_name,
            level=dto.level,
            pros=dto.pros,
            cons=dto.cons,
            chapter_title=dto.chapter_title,
            directional=dto.directional,
            work_experiences=user.work_experiences,
            project_experiences=user.project_experiences
        )))

        answer: ResumeGPT.Response.Answer = resume_helper.get_answer()
        if not answer or not answer.sections:
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)

        return answer.sections[0].content
