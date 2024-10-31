from dataclasses import asdict

from flask import Blueprint, request

from dto.job.job import JobDto

from services.job_service import JobService

job_bp = Blueprint('job', __name__)


@job_bp.route('/job/<occupation_id>', methods=['GET'])
def get_jobs(occupation_id: int):

    jobs = JobService.get_jobs(occupation_id)
    response: JobDto.Response.Jobs = JobDto.Response.Jobs(
        jobs=[JobDto.Response.JobInfo(job.job_id, job.job_name.encode('utf-8').decode('utf-8')) for job in jobs],
    )
    print(response.jobs[0].job_name)

    return asdict(response), 200, {'Content-Type': 'application/json; charset=utf-8'}
