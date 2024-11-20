from http import HTTPStatus
from urllib import request

from flask import Blueprint, request, jsonify, redirect, render_template, flash

from dto.resume.resume import ResumeDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from services.resume_service import ResumeService
from tasks import add_resume_task

resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/', methods=['GET'])
def render_resume():
    return render_template("resume.html")


@resume_bp.route('/write', methods=['GET'])
def render_write():
    task_id = request.args.get('task_id')
    response = None

    if task_id:
        task = add_resume_task.AsyncResult(task_id)
        state = task.state.lower()

        if state == 'success':
            response = task.get()

    return render_template("resume_write.html", response=response)


@resume_bp.route('/write', methods=['POST'])
def create_resume():
    title = request.form.get("title")
    job_id = request.form.get("job_id") or -1
    level = request.form.get("level")
    pros = request.form.get("pros")
    cons = request.form.get("cons")
    is_shared = request.form.get("is_shared") or False
    directional = request.form.get("directional")
    keywords = request.form.getlist("keywords[]")
    section_titles = request.form.getlist("sections[][title]")
    section_contents = request.form.getlist("sections[][content]")
    sections = zip(section_titles, section_contents)

    data = ResumeDto.Request.Create(
        title=title,
        job_id=int(job_id),
        level=level,
        pros=pros,
        cons=cons,
        is_shared=bool(is_shared),
        directional=directional,
        keywords=keywords,
        sections=[ResumeDto.Section(title=title, content=content) for title, content in sections]
    )

    flash_message = data.__validation__()

    if flash_message:
        flash(flash_message)
        return render_template("resume_write.html")

    ResumeService.add_resume(data)
    return redirect("/user/mypage/resume")


@resume_bp.route('/information/all', methods=['GET', 'POST'])
def create_section():
    if request.method == 'POST':
        keywords = request.form.getlist("keywords[]")
        job_id = request.form.get("job_id") or -1
        level = request.form.get("level")
        pros = request.form.get("pros")
        cons = request.form.get("cons")
        directional = request.form.get("directional")
        chapter = request.form.getlist("chapter[]")

        request_resume = ResumeDto.Request.CreateFullResume(
            keywords=keywords,
            job_id=int(job_id),
            level=level,
            pros=pros,
            cons=cons,
            directional=directional,
            chapter=chapter
        )

        flash_message = request_resume.__validation__()

        if flash_message:
            flash(flash_message)
            return render_template("resume_information_all.html")

        task = ResumeService.add_section(request_resume)
        return redirect(f"/resume/waiting?task_id={task.id}")
    else:
        return render_template("resume_information_all.html")


@resume_bp.route('/waiting', methods=['GET'])
def render_waiting():
    task_id = request.args.get('task_id')
    return render_template("resume_waiting.html", task_id=task_id)


@resume_bp.route('/task/<task_id>', methods=['POST'])
def get_task(task_id):
    task = add_resume_task.AsyncResult(task_id)
    state = task.state.lower()

    if state == 'success':
        return jsonify({"task_id": task.id}), HTTPStatus.OK
    elif state == 'failure':
        raise CustomException(ExceptionType.CELERY_ERROR)
    else:
        return {}, HTTPStatus.ACCEPTED
