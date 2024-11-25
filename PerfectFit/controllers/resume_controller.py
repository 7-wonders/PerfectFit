from http import HTTPStatus
from urllib import request

from flask import Blueprint, request, jsonify, redirect, render_template, flash, url_for

from dto.keyword.keyword import KeywordDto
from dto.resume.resume import ResumeDto
from dto.resume.resume_gpt import ResumeGPT
from dto.resume_section.resume_section import ResumeSectionDto
from dto.user.user import UserDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from services.resume_service import ResumeService
from tasks import add_resume_task
from utils.model_converter import model_to_dict
from utils.check_api import is_api_call

resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/', methods=['GET'])
def render_resume():
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 10, type=int)
    sort = request.args.get('sort', 'r', type=str)
    occupation_id = request.args.get('occupation_id', None, type=str)
    job_id = request.args.get('job_id', None, type=str)
    level = request.args.get('level', None, type=str)
    search = request.args.get('search', None, type=str)

    resumes, total = ResumeService.get_resumes(
        page=page,
        count=count,
        sort=sort,
        occupation_id=occupation_id,
        job_id=job_id,
        level=level,
        search=search
    )

    if is_api_call(request):
        response = {
            "resumes": [model_to_dict(resume) for resume in resumes],
            "total": total
        }

        return jsonify(response), HTTPStatus.OK
    else:
        response = {
            "resumes": [model_to_dict(resume) for resume in resumes],
            "total": total
        }

        return render_template("resume_list.html", response=response)


@resume_bp.route('/<resume_id>', methods=['GET'])
def render_resume_detail(resume_id: str):
    if not resume_id.isdecimal():
        redirect(url_for('resume.render_resume'))

    resume, sections, increased_view = ResumeService.get_resume(resume_id)
    if not resume or not sections:
        return redirect(url_for('resume.render_resume'))

    response: ResumeDto.Response.Resume = ResumeDto.Response.Resume(
        resumeId=resume.get('resumeId'),
        title=resume.get('title'),
        level=resume.get('level'),
        jobName=resume.get('jobName'),
        occupationName=resume.get('occupationName'),
        viewCount=resume.get('viewCount') + 1 if increased_view else resume.get('viewCount'),
        likeCount=resume.get('likeCount'),
        createdTime=resume.get('createdTime').strftime('%Y-%m-%d %H:%M:%S'),
        isLike=(
            None if request.cookies.get('access_token') is None
            else
            resume.get('isLike') if 'isLike' in resume else False
        ),
        section=[ResumeSectionDto.Response.Section(
            sectionId=section.get('sectionId'),
            title=section.get('title'),
            content=section.get('content')
        ) for section in sections],
        user=UserDto.Response.IntroUserWithProfile(
            userId=resume.get('user.userId'),
            username=resume.get('user.username'),
            profilePath=resume.get('user.profilePath')
        )
    )

    return render_template("resume_detail.html", response=response)


@resume_bp.route('/<resume_id>/update', methods=['GET', 'POST'])
def render_update_resume(resume_id: str):
    if not resume_id.isdecimal():
        redirect(url_for('resume.render_resume'))

    if request.method == 'POST':
        job_id = request.form.get("job_id")
        title = request.form.get("title")
        level = request.form.get("level")
        pros = request.form.get("pros")
        cons = request.form.get("cons")
        is_shared = request.form.get("is_shared") or False
        directional = request.form.get("directional")
        keyword_ids = request.form.getlist("keywords[][keywordId]")
        keyword_contents = request.form.getlist("keywords[][content]")
        keywords = zip(keyword_ids, keyword_contents)

        section_ids = request.form.getlist("sections[][sectionId]")
        section_titles = request.form.getlist("sections[][title]")
        section_contents = request.form.getlist("sections[][content]")
        sections = zip(section_ids, section_titles, section_contents)

        data = ResumeDto.Request.Update(
            job_id=int(job_id),
            title=title,
            level=level,
            pros=pros,
            cons=cons,
            is_shared=bool(is_shared),
            directional=directional,
            keywords=[KeywordDto.Request.Update(keywordId=keyword_id, content=content)
                      for keyword_id, content in keywords],
            sections=[ResumeSectionDto.Request.Update(section_id=section_id, title=title, content=content)
                      for section_id, title, content in sections]
        )

        flash_message = data.__validation__()
        if flash_message:
            flash(flash_message)
        else:
            ResumeService.update_resume(resume_id, data=data)
            return redirect(f"/resume/{resume_id}")

    response = ResumeService.get_resume_with_update(resume_id)
    if not response:
        return redirect(url_for('resume.render_resume'))

    return render_template("resume_write_update.html", response=response)


@resume_bp.route('/write', methods=['GET'])
def render_write():
    task_id = request.args.get('task_id')
    task_response: ResumeGPT.Response.FullResume.Resume | None = None

    if task_id:
        task = add_resume_task.AsyncResult(task_id)
        state = task.state.lower()

        if state == 'success':
            task_response = task.get()
        elif state == 'failure':
            raise CustomException(ExceptionType.CELERY_ERROR)
        else:
            return redirect(f"/resume/waiting?task_id={task_id}")

    if task_response:
        jobs, occupations = ResumeService.get_resume_write_data(task_response)
        response = ResumeDto.Response.ResumeForWrite(
            resume=task_response,
            jobs=jobs,
            occupations=occupations
        )
    else:
        occupations = ResumeService.get_occupations()
        response = ResumeDto.Response.ResumeForWrite(
            resume=None,
            jobs=None,
            occupations=occupations
        )

    return render_template("resume_write_all.html", response=response)


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
        sections=[ResumeSectionDto.Request.Create(title=title, content=content)
                  for title, content in sections]
    )

    flash_message = data.__validation__()

    if flash_message:
        flash(flash_message)
        return redirect(url_for('resume.render_write'))

    ResumeService.add_resume(data)
    return redirect("/user/mypage/resume")


@resume_bp.route('/write/part', methods=['POST'])
def create_section_content():
    data = request.get_json()

    has_keyword = ('keywords' not in data or not data["keywords"] or len(data["keywords"]) < 1
                   or not any([keyword.strip() for keyword in data["keywords"]]))
    has_job = 'jobId' not in data or not data["jobId"] or data["jobId"] < 1
    has_level = 'level' not in data or not data["level"] or not data["level"] in ["신입", "경력"]
    has_pros = 'pros' not in data or not data["pros"]
    has_cons = 'cons' not in data or not data["cons"]
    has_chapter_title = 'chapterTitle' not in data or not data["chapterTitle"]

    if has_keyword:
        raise CustomException(ExceptionType.REQUIRED_KEYWORDS)
    elif has_job:
        raise CustomException(ExceptionType.REQUIRED_JOB)
    elif has_level:
        raise CustomException(ExceptionType.REQUIRED_LEVEL)
    elif has_pros:
        raise CustomException(ExceptionType.REQUIRED_PROS)
    elif has_cons:
        raise CustomException(ExceptionType.REQUIRED_CONS)
    elif has_chapter_title:
        raise CustomException(ExceptionType.REQUIRED_CHAPTER_TITLE)

    dto = ResumeDto.Request.CreateSectionContent(
        keywords=data["keywords"],
        job_id=data["jobId"],
        level=data["level"],
        pros=data["pros"],
        cons=data["cons"],
        chapter_title=data["chapterTitle"],
        directional=data["directional"]
    )

    content = ResumeService.add_section_content(dto)
    return jsonify({"content": content}), HTTPStatus.OK


@resume_bp.route('/information', methods=['GET', 'POST'])
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
    return render_template("resume_loading.html", task_id=task_id)


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


@resume_bp.route('/<resume_id>/like', methods=['POST', 'DELETE'])
def like_resume(resume_id: str):
    if not resume_id.isdecimal():
        return CustomException(ExceptionType.INVALID_RESUME_ID)

    if request.method == 'POST':
        ResumeService.like_resume(resume_id, True)
    elif request.method == 'DELETE':
        ResumeService.like_resume(resume_id, False)

    return jsonify({}), HTTPStatus.NO_CONTENT


@resume_bp.route('/<resume_id>', methods=['DELETE'])
def delete_resume(resume_id: str):
    if not resume_id.isdecimal():
        return CustomException(ExceptionType.INVALID_RESUME_ID)

    ResumeService.delete_resume(int(resume_id))
    return jsonify({}), HTTPStatus.NO_CONTENT


@resume_bp.route('/select')
def get_resume_select():
    return render_template("resume_select.html")
