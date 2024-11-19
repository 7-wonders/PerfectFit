from http import HTTPStatus

from flask import Blueprint, request, jsonify, redirect, session, render_template

from dto.resume.resume import ResumeDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from services.resume_service import ResumeService
from tasks import add_resume_task

resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/write', methods=['GET'])
def render_write():
    task_id = request.args.get('task_id')

    if task_id is None:
        return redirect('/resume')

    task = add_resume_task.AsyncResult(task_id)
    state = task.state.lower()

    if state == 'success':
        response = task.get()
        # 전체 작성 페이지 HTMl 변경 요망
        return render_template("test.html", response=response)
    else:
        return redirect('/resume')


@resume_bp.route('/write/all', methods=['POST'])
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
    state = task.state.lower()

    if state == 'success':
        return redirect(f'/resume/write/all?task_id={task_id}')
    elif state == 'failure':
        raise CustomException(ExceptionType.CELERY_ERROR)
    else:
        return jsonify({"status": "running"}), HTTPStatus.ACCEPTED
