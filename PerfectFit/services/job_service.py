from flask import flash, abort
from flask_sqlalchemy.pagination import Pagination

from database.config import get_session
from domain.models import Job, Occupation
from dto.job.job import JobDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType


class JobService:
    @staticmethod
    def get_jobs(occupation_id: int) -> list[Job]:
        jobs = get_session().query(Job).filter(Job.occupation_id == occupation_id).all()

        if not jobs :
            raise CustomException(ExceptionType.NOT_FOUND_JOB)
        return jobs

    @staticmethod
    def get_jobs_info(occupation_id: int) -> JobDto.Response.Jobs:
        jobs = get_session().query(Job).filter(Job.occupation_id == occupation_id).all()

        response: JobDto.Response.Jobs = JobDto.Response.Jobs(
            jobs=[JobDto.Response.JobInfo(job.job_id, job.job_name.encode('utf-8').decode('utf-8')) for job in jobs],
        )

        return response


    @staticmethod
    def get_occupations() -> list[Occupation]:
        occupations = get_session().query(Occupation).all()

        if not occupations :
            raise CustomException(ExceptionType.NOT_FOUND_OCCUPATION)
        return occupations
