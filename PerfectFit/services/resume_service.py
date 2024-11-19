from celery.exceptions import NotRegistered
from flask import request
from kombu.exceptions import OperationalError
from sqlalchemy.orm import joinedload

from config.config_mysql import get_session
from domain.models import Job, AppUser, ProjectExperience
from dto.resume.resume import ResumeDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from utils.jwt_factory import JWTFactory
from tasks import add_resume_task

logger = Logger(__name__)


class ResumeService:
    @staticmethod
    def add_resume(resume: ResumeDto.Request.CreateFullResume):
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
