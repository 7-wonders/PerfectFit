from celery.exceptions import NotRegistered
from flask import request
from kombu.exceptions import OperationalError
from sqlalchemy.orm import joinedload

from config.config_mysql import get_session
from domain.models import Job, AppUser, ProjectExperience, Resume, ProsCons, ResumeSection, Keyword
from dto.resume.resume import ResumeDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from utils.jwt_factory import JWTFactory
from tasks import add_resume_task

logger = Logger(__name__)


class ResumeService:
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
            logger.error("Celery 실행 도중 에러가 발생하였습니다." , e)
            raise CustomException(ExceptionType.CELERY_ERROR)
