
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
import time

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

        return render_template("resume.html", response=response)


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

    return render_template("resume_update.html", response=response)


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

# @resume_bp.route('/write/part', methods=['POST'])
# def get_resume_write_part():
#     # 요청 데이터 받기
#     data = request.json

#     # 요청 데이터 확인 (로깅용)
#     print("Received data:", data)

#     #작성하기 애니메이션을 보기 위한 5초 지연
#     time.sleep(5);

#     # 더미 응답 데이터 생성
#     response_data = {
#         "content": (
#             f"안녕하세요. 저는 {data.get('level', '신입')}이며, "
#             f"{data.get('pros', '장점')}을 가지고 있습니다. "
#             f"하지만 {data.get('cons', '단점')}이 있습니다. "
#             f"저의 목표는 '{data.get('directional', '특정 방향 없음')}' 방향성을 가지고 "
#             f"최고의 성과를 내는 것입니다."
#         )
#     }
#     # JSON 응답 반환
#     return jsonify(response_data), 200

# @resume_bp.route('/job/<int:occupation_id>', methods=['GET'])
# def get_jobs(occupation_id):
#     # 더미 데이터
#     job_data = {
#         1: [
#             {"jobId": 101, "jobName": "Software Engineer"},
#             {"jobId": 102, "jobName": "Data Scientist"},
#         ],
#         2: [
#             {"jobId": 201, "jobName": "Mechanical Engineer"},
#             {"jobId": 202, "jobName": "Civil Engineer"},
#         ],
#         3: [
#             {"jobId": 301, "jobName": "Accountant"},
#             {"jobId": 302, "jobName": "Auditor"},
#         ]
#     }

#     # occupation_id에 해당하는 직업 목록 가져오기
#     jobs = job_data.get(occupation_id, [])

#     # 응답 데이터 생성
#     response = {
#         "jobs": jobs
#     }

#     # JSON 데이터 반환
#     return jsonify(response), 200

# @resume_bp.route('/write')
# def get_resume_write():
#     return render_template("resume_write_all.html")

# @resume_bp.route('/<int:resumeNum>/update')
# def get_resume_write_update(resumeNum):
#     return render_template("resume_write_update.html", resumeNum=resumeNum)

# @resume_bp.route('/select')
# def get_resume_select():
#     return render_template("resume_select.html")

# @resume_bp.route('/information')
# def get_resume_information():
#     return render_template("resume_information_all.html")

# @resume_bp.route('/loading')
# def get_resume_load_loading():
#     return render_template("resume_loading.html")

# @resume_bp.route('/test')
# def get_test():
#     return render_template("textAxios.html")

# @resume_bp.route('/list/<int:page>')
# def get_resume_list(page):
#     total = 100
#     return render_template("resume_list.html", total=total, page=page)

# @resume_bp.route('/detail/<int:resume_id>')
# def get_resume_detail(resume_id):
#     total = 100
#     return render_template("resume_detail.html", total=total)


# # 자기소개서 상세보기 페이지네이션 버튼 누를 시 동작
# @resume_bp.route('/test/list/<int:page>', methods=['GET'])
# def get_resume_list_test(page):
#     resumes = [
#         {
#             "resumeId": 1,
#             "title": "API 자기소개서1",
#             "occupationName": "Developer",
#             "jobName": "Software Engineer",
#             "level": "경력",
#             "user": {
#                 "username": "john_doe",
#                 "profilePath": url_for('static', filename='img/logo.svg')
#             },
#             "viewCount": 100,
#             "likeCount": 50,
#             "createdTime": "2024-11-21T12:34:56"
#         },
#         {
#             "resumeId": 2,
#             "title": "API 자기소개서2",
#             "occupationName": "Designer",
#             "jobName": "UI/UX Designer",
#             "level": "경력",
#             "user": {
#                 "username": "jane_doe",
#                 "profilePath": url_for('static', filename='img/logo.svg')
#             },
#             "viewCount": 80,
#             "likeCount": 30,
#             "createdTime": "2024-11-20T11:20:45"
#         },
#         {
#             "resumeId": 3,
#             "title": "API 자기소개서3",
#             "occupationName": "Designer",
#             "jobName": "UI/UX Designer",
#             "level": "신입",
#             "user": {
#                 "username": "jane_doe",
#                 "profilePath": url_for('static', filename='img/logo.svg')
#             },
#             "viewCount": 80,
#             "likeCount": 30,
#             "createdTime": "2024-11-20T11:20:45"
#         },
#         {
#             "resumeId": 4,
#             "title": "API 자기소개서4",
#             "occupationName": "Designer",
#             "jobName": "UI/UX Designer",
#             "level": "신입",
#             "user": {
#                 "username": "jane_doe",
#                 "profilePath": url_for('static', filename='img/logo.svg')
#             },
#             "viewCount": 80,
#             "likeCount": 30,
#             "createdTime": "2024-11-20T11:20:45"
#         },
#         {
#             "resumeId": 5,
#             "title": "API 자기소개서5",
#             "occupationName": "Designer",
#             "jobName": "UI/UX Designer",
#             "level": "신입",
#             "user": {
#                 "username": "jane_doe",
#                 "profilePath": url_for('static', filename='img/logo.svg')
#             },
#             "viewCount": 80,
#             "likeCount": 30,
#             "createdTime": "2024-11-20T11:20:45"
#         }
#         # 여기에 더 많은 resume 객체를 추가할 수 있습니다.
#     ]

#     # 응답 데이터
#     response = {
#         "resumes": resumes
#     }

#     return jsonify(response), 200
