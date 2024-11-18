from flask import Blueprint, request, jsonify, redirect

from dto.resume.resume import ResumeDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from services.resume_service import ResumeService
from tasks import add_resume_task

resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/', methods=['POST'])
def create_resume():
    data = request.get_json()
    request_resume = ResumeDto.Request.CreateFullResume(**data)

    if not request_resume.keywords:
        return CustomException(ExceptionType.REQUIRED_KEYWORDS)
    elif not request_resume.job_id:
        return CustomException(ExceptionType.REQUIRED_JOB)
    elif not request_resume.level:
        return CustomException(ExceptionType.REQUIRED_LEVEL)
    elif not request_resume.pros:
        return CustomException(ExceptionType.REQUIRED_PROS)
    elif not request_resume.cons:
        return CustomException(ExceptionType.REQUIRED_CONS)

    task = ResumeService.add_resume(request_resume)

    return redirect(f"/resume/waiting?task_id={task.id}")


@resume_bp.route('/task/<task_id>', methods=['POST'])
def get_task(task_id):
    task = add_resume_task.AsyncResult(task_id)

    if task.state == 'SUCCESS':
        return jsonify(task.get())
    else:
        return jsonify({"status": "running"})
