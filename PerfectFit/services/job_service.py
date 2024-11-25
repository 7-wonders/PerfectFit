import json
from dataclasses import asdict

from config.config_mysql import get_session

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

    @staticmethod
    def get_all():
        occupations: list[Occupation] = JobService.get_occupations()

        response: JobDto.Response.OccupationsWithJob = JobDto.Response.OccupationsWithJob(
            occupations=[JobDto.Response.OccupationInfoWithJob(
                occupationId=occupation.occupation_id,
                occupationName=occupation.occupation_name,
                majorCategory=occupation.major_category,
                subCategory=occupation.sub_category)
                for occupation in occupations],
        )
        for i, occupation in enumerate(response.occupations):
            jobs_info: JobDto.Response.Jobs = JobService.get_jobs_info(occupation.occupationId)

            response.occupations[i].jobs = jobs_info.jobs
            response.occupations[i].total = len(jobs_info.jobs)

        json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

        return response