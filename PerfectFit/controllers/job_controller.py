import json
from dataclasses import asdict

from flask import Blueprint, request, jsonify, Response

from domain.models import Occupation, Job
from dto.job.job import JobDto

from services.job_service import JobService

job_bp = Blueprint('job', __name__)


@job_bp.route('/job/<occupation_id>', methods=['GET'])
def get_jobs(occupation_id: int):

    jobs:list[Job] = JobService.get_jobs(occupation_id)

    response: JobDto.Response.Jobs = JobDto.Response.Jobs(
        jobs=[JobDto.Response.JobInfo(
            jobId=job.job_id,
            jobName=job.job_name.encode('utf-8').decode('utf-8')) for job in jobs], # 인코딩
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)



    return Response(json_response, status=200, content_type='application/json; charset=utf-8')


@job_bp.route('/job/occupation', methods=['GET'])
def get_occupations():

    occupations:list[Occupation] = JobService.get_occupations()

    response: JobDto.Response.Occupations = JobDto.Response.Occupations(
        occupations=[JobDto.Response.OccupationInfo(
            occupationId=occupation.occupation_id,
            occupationName=occupation.occupation_name,
            majorCategory=occupation.major_category,
            subCategory=occupation.sub_category)
         for occupation in occupations],
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')
@job_bp.route('/job', methods=['GET'])
def get_all():

    occupations:list[Occupation] = JobService.get_occupations()

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

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')
