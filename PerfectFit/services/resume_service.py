from flask import g, request
from sqlalchemy.orm import joinedload

from config.config_mysql import get_session
from domain.models import Job, AppUser, ProjectExperience
from dto.resume.resume import ResumeDto
from dto.resume.resume_gpt import ResumeGPT
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from utils.jwt_factory import JWTFactory
from utils.openai.resume.full_resume_strategy import FullResumeStrategy
from utils.openai.resume.resume_helper import ResumeHelper


class ResumeService:
    @staticmethod
    def _add_resume_with_gpt(job_name: str, user: AppUser, resume: ResumeDto.Request.CreateFullResume) -> None:
        resume_helper = ResumeHelper(strategy=FullResumeStrategy(resume=ResumeGPT.Request.CreateResume(
            keywords=resume.keywords,
            job_name=job_name,
            level=resume.level,
            pros=resume.pros,
            cons=resume.cons,
            directional=resume.directional,
            chapter=resume.chapter,
            work_experiences=user.work_experiences,
            project_experiences=user.project_experiences
        )))

        return resume_helper.get_answer()

    @staticmethod
    def add_resume(resume: ResumeDto.Request.CreateFullResume) -> ResumeGPT.Response.Resume:
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