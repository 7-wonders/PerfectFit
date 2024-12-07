from celery.exceptions import NotRegistered
from flask import request, flash
from kombu.exceptions import OperationalError
from sqlalchemy import func, select, RowMapping
from sqlalchemy.orm import joinedload

from config.config_mysql import get_session
from domain.models import Job, AppUser, ProjectExperience, Resume, ProsCons, ResumeSection, Keyword, ResumeView, \
    ResumeLike, Occupation
from domain.models.resume_draft import ResumeDraft
from dto.keyword.keyword import KeywordDto
from dto.resume.resume import ResumeDto
from dto.resume.resume_gpt import ResumeGPT
from dto.resume_section.resume_section import ResumeSectionDto
from dto.user.user import UserDto
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
    def get_intro_drafts(user_id: int):
        with get_session() as session:
            query = (
                select(
                    ResumeDraft.draft_id,
                    ResumeDraft.title,
                    ResumeDraft.created_time
                )
                .where(ResumeDraft.user_id == user_id)
                .order_by(ResumeDraft.draft_id.desc())
            )

            resume_drafts = session.execute(query).mappings().all()
            return resume_drafts


    @staticmethod
    def get_resumes(**kwargs):
        with (get_session() as session):
            page = kwargs.get('page', 1)
            count = kwargs.get('count', 10)
            job_id = kwargs.get('job_id')
            occupation_id = kwargs.get('occupation_id')
            level = kwargs.get('level')
            search = kwargs.get('search')

            view_scalar_query = (
                select(func.count(ResumeView.view_id))
                .where(ResumeView.resume_id == Resume.resume_id)
                .scalar_subquery()
            )

            like_scalar_query = (
                select(func.count(ResumeLike.like_id))
                .where(ResumeLike.resume_id == Resume.resume_id)
                .scalar_subquery()
            )

            search_where_clause = Resume.title.like(f"%{search}%") if search else True
            level_where_clause = Resume.level == level if level else True
            job_where_clause = Job.job_id == job_id if job_id else True
            occupation_where_clause = Occupation.occupation_id == occupation_id if occupation_id else True

            order_by_value = [view_scalar_query.desc(), Resume.created_time.desc()] \
                if kwargs.get('sort') == 'f' else [Resume.created_time.desc()]

            query = (
                select(
                    Resume.resume_id.label('resumeId'),
                    Resume.title,
                    Resume.level,
                    Resume.created_time.label('createdTime'),
                    like_scalar_query.label('likeCount'),
                    view_scalar_query.label('viewCount'),
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
    def get_my_resumes(user_id: int, page: int, count: int):
        session = get_session()

        # 자기소개서 목록을 가져오기 위한 쿼리
        resumes_query = session.query(Resume).filter(Resume.user_id == user_id)
        total = resumes_query.count()

        resumes = resumes_query.order_by(Resume.created_time.desc()) \
                               .offset((page - 1) * count) \
                               .limit(count) \
                               .all()

        # 조회수 및 좋아요 수 계산
        for resume in resumes:
            resume.view_count = session.query(func.sum(ResumeView.view_count)).filter(
                ResumeView.resume_id == resume.resume_id
            ).scalar() or 0

            resume.like_count = session.query(func.sum(ResumeLike.like_count)).filter(
                ResumeLike.resume_id == resume.resume_id
            ).scalar() or 0

        return resumes, total

    @staticmethod
    def get_resume_write_data(task_data: ResumeGPT.Response.FullResume.Resume = None):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

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
            resume_intro_drafts = ResumeService.get_intro_drafts(user_id)

            return jobs, occupations, resume_intro_drafts

    @staticmethod
    def get_resume_write_without_data():
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            query = (
                select(
                    Occupation.occupation_id.label('occupationId'),
                    Occupation.occupation_name.label('occupationName')
                )
            )

            occupations = session.execute(query).mappings().all()
            resume_intro_drafts = ResumeService.get_intro_drafts(user_id)

            return occupations, resume_intro_drafts

    @staticmethod
    def get_resume(resume_id: str) -> Resume | None:
        access_token = request.cookies.get('access_token')
        user_id = None
        increased_view = False

        if access_token:
            user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            is_like_scalar_query = func.exists(
                select(1)
                .where(ResumeLike.user_id == user_id, ResumeLike.resume_id == Resume.resume_id)
            )

            is_view_scalar_query = func.exists(
                select(1)
                .where(ResumeView.user_id == user_id, ResumeView.resume_id == Resume.resume_id)
            )

            like_scalar_query = (
                select(func.count(ResumeLike.like_id))
                .where(ResumeLike.resume_id == Resume.resume_id)
                .correlate(Resume)
                .scalar_subquery()
            )

            view_scalar_query = (
                select(func.count(ResumeView.view_id))
                .where(ResumeView.resume_id == Resume.resume_id)
                .correlate(Resume)
                .scalar_subquery()
            )

            columns = [
                Resume.resume_id.label('resumeId'),
                Resume.title,
                Resume.level,
                Resume.created_time.label('createdTime'),
                like_scalar_query.label('likeCount'),
                view_scalar_query.label('viewCount'),
                AppUser.user_id.label('user.userId'),
                AppUser.username.label('user.username'),
                AppUser.profile_path.label('user.profilePath'),
                Job.job_name.label('jobName'),
                Occupation.occupation_name.label('occupationName'),
            ]

            if user_id:
                columns.append(is_like_scalar_query.label('isLike'))
                columns.append(is_view_scalar_query.label('isView'))

            resume_query = (
                select(*columns)
                .join(Job, Job.job_id == Resume.job_id)
                .join(Occupation, Occupation.occupation_id == Job.occupation_id)
                .join(AppUser, AppUser.user_id == Resume.user_id)
                .filter(Resume.resume_id == resume_id, Resume.is_shared.is_(True))
            )

            resume = session.execute(resume_query).mappings().first()

            if not resume:
                return None

            sections_query = (
                select(
                    ResumeSection.resume_section_id.label('sectionId'),
                    ResumeSection.title,
                    ResumeSection.content
                )
                .filter(ResumeSection.resume_id == resume_id)
            )

            sections = session.execute(sections_query).mappings().all()
            if not sections:
                return None

            if user_id and resume.get('user.userId') != user_id and not resume.get('isView'):
                session.add(ResumeView(
                    user_id=user_id,
                    resume_id=resume.resumeId
                ))

                session.commit()
                increased_view = True

            response: ResumeDto.Response.Resume = ResumeDto.Response.Resume(
                resumeId=resume.get('resumeId'),
                title=resume.get('title'),
                level=resume.get('level'),
                jobName=resume.get('jobName'),
                occupationName=resume.get('occupationName'),
                viewCount=resume.get('viewCount') + 1 if increased_view else resume.get('viewCount'),
                likeCount=resume.get('likeCount'),
                createdTime=resume.get('createdTime').strftime('%Y-%m-%d %H:%M:%S'),
                isMine=resume.get('user.userId') == user_id,
                isLike=(
                    None if request.cookies.get('access_token') is None
                    else
                    resume.get('isLike') if 'isLike' in resume else False
                ),
                section=[ResumeSectionDto.Response.Section(
                    sectionId=section.get('sectionId'),
                    title=section.get('title'),
                    content=section.get('content')
                ) for section in sections],
                user=UserDto.Response.IntroUserWithProfile(
                    userId=resume.get('user.userId'),
                    username=resume.get('user.username'),
                    profilePath=resume.get('user.profilePath')
                )
            )

            print(response)

            return response

    @staticmethod
    def get_resume_with_update(resume_id: str):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))
        if not user_id:
            flash('로그인이 필요합니다.', 'danger')
            return None

        with (get_session() as session):
            pros_subquery = (
                select(ProsCons.content)
                .where(ProsCons.resume_id == resume_id)
                .where(ProsCons.type == 'pros')
                .scalar_subquery()
            )

            cons_subquery = (
                select(ProsCons.content)
                .where(ProsCons.resume_id == resume_id)
                .where(ProsCons.type == 'cons')
                .scalar_subquery()
            )

            resume_query = (
                select(
                    Resume.user_id.label('userId'),
                    Resume.resume_id.label('resumeId'),
                    Resume.job_id.label('jobId'),
                    Resume.title,
                    Resume.level,
                    Resume.directional,
                    Resume.is_shared.label('isPublic'),
                    pros_subquery.label('pros'),
                    cons_subquery.label('cons')
                )
                .filter(Resume.resume_id == resume_id)
            )

            resume = session.execute(resume_query).mappings().first()
            if not resume:
                flash('자기소개서 정보를 불러오는 중 오류가 발생했습니다.', 'danger')
                return None

            job_id = resume.get('jobId')
            pros = resume.get('pros')
            cons = resume.get('cons')

            if not job_id or not pros or not cons:
                flash('자기소개서 정보를 불러오는 중 오류가 발생했습니다.', 'danger')
                return None

            if resume.get('userId') != user_id:
                flash('본인의 자기소개서만 수정할 수 있습니다.', 'danger')
                return None

            sections_query = (
                select(
                    ResumeSection.resume_section_id.label('sectionId'),
                    ResumeSection.title,
                    ResumeSection.content
                )
                .filter(ResumeSection.resume_id == resume_id)
            )

            sections = session.execute(sections_query).mappings().all()
            if not sections:
                return None

            keywords_query = (
                select(
                    Keyword.keyword_id.label('keywordId'),
                    Keyword.content
                )
                .filter(Keyword.resume_id == resume_id)
            )

            keywords = session.execute(keywords_query).mappings().all()
            if not keywords:
                flash('자기소개서 정보를 불러오는 중 오류가 발생했습니다.', 'danger')
                return None

            selected_job_query = (
                select(
                    Job.occupation_id
                )
                .where(Job.job_id == job_id)
                .scalar_subquery()
            )

            job_query = (
                select(
                    Job.job_id.label('jobId'),
                    Job.job_name.label('jobName'),
                    (
                            Job.job_id == job_id
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

            response = ResumeDto.Response.ResumeForUpdate(
                resume=ResumeDto.Response.ResumeWithUpdate(
                    resumeId=resume.get('resumeId'),
                    title=resume.get('title'),
                    level=resume.get('level'),
                    pros=pros,
                    cons=cons,
                    keywords=[
                        KeywordDto.Response.Keyword(
                            keywordId=keyword.get('keywordId'),
                            content=keyword.get('content')
                        )
                        for keyword in keywords
                    ],
                    directional=resume.get('directional'),
                    sections=[
                        ResumeSectionDto.Response.Section(
                            sectionId=section.get('sectionId'),
                            title=section.get('title'),
                            content=section.get('content')
                        )
                        for section in sections
                    ],
                    isPublic=resume.get('isPublic')
                ),
                jobs=jobs,
                occupations=occupations
            )

            return response

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
                type='pros',
                content=request_resume.pros,
            )

            cons = ProsCons(
                resume_id=resume.resume_id,
                type='cons',
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

            if request_resume.draft_id:
                session.query(ResumeDraft).filter(ResumeDraft.draft_id == request_resume.draft_id).delete()
                session.query(ResumeSection).filter(ResumeSection.draft_id == request_resume.draft_id).delete()
                session.query(Keyword).filter(Keyword.draft_id == request_resume.draft_id).delete()
                session.query(ProsCons).filter(ProsCons.draft_id == request_resume.draft_id).delete()

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

    @staticmethod
    def update_resume(resume_id: str, data: ResumeDto.Request.Update):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with (get_session() as session):
            resume = session.query(Resume).filter(Resume.resume_id == resume_id).first()
            if not resume:
                flash('자기소개서를 찾을 수 없습니다.', 'danger')
                return None

            if resume.user_id != user_id:
                flash('잘못된 접근입니다.', 'danger')
                return None

            job = session.query(Job).filter(Job.job_id == data.job_id).first()
            if not job:
                flash('유효하지 않은 직업 ID입니다.', 'danger')
                return None

            resume.title = data.title
            resume.job_id = data.job_id
            resume.level = data.level
            resume.directional = data.directional \
                if data.directional not in ["None", None, "", "null"] else None
            resume.is_shared = data.is_shared

            pros = session.query(ProsCons).filter(ProsCons.resume_id == resume_id, ProsCons.type == 'pros').first()
            if pros:
                pros.content = data.pros

            cons = session.query(ProsCons).filter(ProsCons.resume_id == resume_id, ProsCons.type == 'cons').first()
            if cons:
                cons.content = data.cons

            session.query(Keyword).filter(Keyword.resume_id == resume_id).delete()
            keywords = [
                Keyword(
                    resume_id=resume_id,
                    job_id=data.job_id,
                    content=keyword.content
                )
                for keyword in data.keywords
            ]
            session.add_all(keywords)

            db_section = session.query(ResumeSection).filter(ResumeSection.resume_id == resume_id).all()
            new_sections = []

            # 사용자가 추가한 섹션 ID 기준으로 나누기
            data_sections_by_id = {int(section.section_id): section
                                   for section in data.sections
                                   if section.section_id not in [None, "None", "", "null"]}
            # DB에 저장된 섹션 ID 기준으로 나누기
            db_sections = {section.resume_section_id: section
                           for section in db_section}
            # 사용자가 추가한 섹션
            new_sections_by_data = [section
                                    for section in data.sections
                                    if section.section_id in [None, "None", "", "null"]]

            db_sections_ids = set(db_sections.keys())
            data_sections_ids = set(data_sections_by_id.keys())

            # 사용자가 추가한 섹션 ID가 DB에 저장된 섹션 ID에 포함되지 않았다면 삭제
            for section_id in db_sections_ids - data_sections_ids:
                session.delete(db_sections[section_id])

            # 사용자가 추가한 섹션 ID가 DB에 저장된 섹션 ID에 포함되어 있다면 수정
            for section_id in db_sections_ids & data_sections_ids:
                if not db_sections[section_id].title.strip() \
                        or not db_sections[section_id].content.strip():
                    continue

                db_section = db_sections[section_id]
                db_section.title = data_sections_by_id[section_id].title
                db_section.content = data_sections_by_id[section_id].content

            # 사용자가 추가한 섹션 ID가 DB에 저장된 섹션 ID에 포함되지 않았다면 추가
            for section in new_sections_by_data:
                if not section.title.strip() or not section.content.strip():
                    continue

                new_sections.append(ResumeSection(
                    resume_id=resume_id,
                    title=section.title,
                    content=section.content
                ))

            session.add_all(new_sections)
            session.commit()

    @staticmethod
    def like_resume(resume_id: str, is_like: bool):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            if is_like:
                like = session.query(ResumeLike).filter(
                    ResumeLike.user_id == user_id,
                    ResumeLike.resume_id == resume_id
                ).first()

                if like:
                    raise CustomException(ExceptionType.ALREADY_LIKED)

                session.add(ResumeLike(
                    user_id=user_id,
                    resume_id=resume_id
                ))
            else:
                session.query(ResumeLike).filter(
                    ResumeLike.user_id == user_id,
                    ResumeLike.resume_id == resume_id
                ).delete()

            session.commit()

    @staticmethod
    def delete_resume(resume_id: int):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            resume = session.query(Resume).filter(Resume.resume_id == resume_id).first()
            if not resume:
                raise CustomException(ExceptionType.NOT_FOUND_RESUME)

            if resume.user_id != user_id:
                raise CustomException(ExceptionType.FORBIDDEN_RESUME)

            session.query(Resume).filter(Resume.resume_id == resume_id).delete()
            session.commit()
