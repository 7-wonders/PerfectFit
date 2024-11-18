from flask import request
from sqlalchemy.orm import joinedload

from config.config_mysql import get_session
from domain.models import Job, AppUser, ProjectExperience
from dto.resume.resume import ResumeDto
from dto.resume.resume_gpt import ResumeGPT
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from utils.jwt_factory import JWTFactory
from tasks import add_resume_task


class ResumeService:
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

        task = add_resume_task.apply_async(kwargs={
            "job_name": job.job_name,
            "user": user,
            "resume": resume
        })

        return task
