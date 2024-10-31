from flask import flash, abort
from flask_sqlalchemy.pagination import Pagination

from database.config import get_session
from domain.models import Job
from domain.models.app_user import AppUser
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType


class JobService:
    @staticmethod
    def get_jobs(occupation_id: int) -> list[Job]:
        jobs = get_session().query(Job).filter(Job.occupation_id == occupation_id).all()

        if not jobs :
            raise CustomException(ExceptionType.NOT_FOUND_JOB)
        return jobs

