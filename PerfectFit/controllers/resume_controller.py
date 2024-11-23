from flask import Blueprint, render_template, url_for
# 더미 데이터를 위한 import
from flask import request, jsonify
import time

resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/write/part', methods=['POST'])
def get_resume_write_part():
    # 요청 데이터 받기
    data = request.json

    # 요청 데이터 확인 (로깅용)
    print("Received data:", data)

    #작성하기 애니메이션을 보기 위한 5초 지연
    time.sleep(5);

    # 더미 응답 데이터 생성
    response_data = {
        "content": (
            f"안녕하세요. 저는 {data.get('level', '신입')}이며, "
            f"{data.get('pros', '장점')}을 가지고 있습니다. "
            f"하지만 {data.get('cons', '단점')}이 있습니다. "
            f"저의 목표는 '{data.get('directional', '특정 방향 없음')}' 방향성을 가지고 "
            f"최고의 성과를 내는 것입니다."
        )
    }
    # JSON 응답 반환
    return jsonify(response_data), 200

@resume_bp.route('/job/<int:occupation_id>', methods=['GET'])
def get_jobs(occupation_id):
    # 더미 데이터
    job_data = {
        1: [
            {"jobId": 101, "jobName": "Software Engineer"},
            {"jobId": 102, "jobName": "Data Scientist"},
        ],
        2: [
            {"jobId": 201, "jobName": "Mechanical Engineer"},
            {"jobId": 202, "jobName": "Civil Engineer"},
        ],
        3: [
            {"jobId": 301, "jobName": "Accountant"},
            {"jobId": 302, "jobName": "Auditor"},
        ]
    }

    # occupation_id에 해당하는 직업 목록 가져오기
    jobs = job_data.get(occupation_id, [])

    # 응답 데이터 생성
    response = {
        "jobs": jobs
    }

    # JSON 데이터 반환
    return jsonify(response), 200

@resume_bp.route('/write/all')
def get_resume_write_all():
    return render_template("resume_write_all.html")

@resume_bp.route('/write/update/<int:resumeNum>')
def get_resume_write_update(resumeNum):
    return render_template("resume_write_update.html", resumeNum=resumeNum)

@resume_bp.route('/select')
def get_resume_select():
    return render_template("resume_select.html")

@resume_bp.route('/information/all')
def get_resume_information_all():
    return render_template("resume_information_all.html")

@resume_bp.route('/information/part')
def get_resume_information_part():
    return render_template("resume_information_part.html")

@resume_bp.route('/loading')
def get_resume_load_loading():
    return render_template("resume_loading.html")

@resume_bp.route('/test')
def get_test():
    return render_template("textAxios.html")

@resume_bp.route('/list/<int:page>')
def get_resume_list(page):
    totalItems = 100  # 예시: 전체 항목의 수
    pageRange = 5  # 한 번에 표시할 페이지 범위
    totalPages = (totalItems + pageRange - 1) // pageRange  # 전체 페이지 수 계산
    return render_template("resume_list.html", page=page, totalPages=totalPages, pageRange=pageRange)

@resume_bp.route('/detail/<int:resume_id>')
def get_resume_detail(resume_id):
    totalItems = 100  # 예시: 전체 항목의 수
    return render_template("resume_detail.html", totalItems=totalItems)


@resume_bp.route('/test/list/<int:page>', methods=['GET'])
def get_resume_list_test(page):
    # 예시: 데이터베이스에서 해당 페이지에 맞는 데이터를 가져옵니다.
    resumes = [
        {
            "resumeId": 1,
            "title": "API 자기소개서1",
            "occupationName": "Developer",
            "jobName": "Software Engineer",
            "level": "경력",
            "user": {
                "username": "john_doe",
                "profilePath": url_for('static', filename='img/logo.svg')
            },
            "viewCount": 100,
            "likeCount": 50,
            "createdTime": "2024-11-21T12:34:56"
        },
        {
            "resumeId": 2,
            "title": "API 자기소개서2",
            "occupationName": "Designer",
            "jobName": "UI/UX Designer",
            "level": "경력",
            "user": {
                "username": "jane_doe",
                "profilePath": url_for('static', filename='img/logo.svg')
            },
            "viewCount": 80,
            "likeCount": 30,
            "createdTime": "2024-11-20T11:20:45"
        },
        {
            "resumeId": 3,
            "title": "API 자기소개서3",
            "occupationName": "Designer",
            "jobName": "UI/UX Designer",
            "level": "신입",
            "user": {
                "username": "jane_doe",
                "profilePath": url_for('static', filename='img/logo.svg')
            },
            "viewCount": 80,
            "likeCount": 30,
            "createdTime": "2024-11-20T11:20:45"
        },
        {
            "resumeId": 4,
            "title": "API 자기소개서4",
            "occupationName": "Designer",
            "jobName": "UI/UX Designer",
            "level": "신입",
            "user": {
                "username": "jane_doe",
                "profilePath": url_for('static', filename='img/logo.svg')
            },
            "viewCount": 80,
            "likeCount": 30,
            "createdTime": "2024-11-20T11:20:45"
        },
        {
            "resumeId": 5,
            "title": "API 자기소개서5",
            "occupationName": "Designer",
            "jobName": "UI/UX Designer",
            "level": "신입",
            "user": {
                "username": "jane_doe",
                "profilePath": url_for('static', filename='img/logo.svg')
            },
            "viewCount": 80,
            "likeCount": 30,
            "createdTime": "2024-11-20T11:20:45"
        }
        # 여기에 더 많은 resume 객체를 추가할 수 있습니다.
    ]

    # 응답 데이터
    response = {
        "resumes": resumes
    }

    return jsonify(response), 200