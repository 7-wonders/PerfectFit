import os
from dataclasses import asdict
import json
from flask import Blueprint, render_template, request, Response, current_app
from werkzeug.utils import secure_filename
from dto.ProjectExperience.projectExperience import PexDTO
from services.user_service import UserService, ResumeService, InterviewService, RequirementsService, \
    NecessaryInfoService, OptionalInfoService, VerificationService
from flask import Blueprint, render_template, request, redirect, make_response
from dto.user.user import UserDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from services.user_service import UserService
from utils.const import const
from utils.jwt_factory import JWTFactory

user_bp = Blueprint('user', __name__)

def get_pagination_params():
    """공통적으로 페이지네이션 파라미터를 가져오는 함수"""
    page = request.args.get('page', default=1, type=int)
    count = request.args.get('count', default=10, type=int)
    return page, count

@user_bp.route('/users')
def get_users():
    page, count = get_pagination_params()  # 페이지네이션 파라미터 함수 사용

    paginate_user = UserService.get_users(page, count)
    response: UserDto.Response.Users = UserDto.Response.Users(
        users=[UserDto.Response.IntroUser(user.user_id, user.username) for user in paginate_user.items],
        pages=paginate_user.pages,
    )

    return render_template("users.html", users=asdict(response))

@user_bp.route('/user/<user_id>')
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    response: UserDto.Response.IntroUser = UserDto.Response.IntroUser(user.id, user.name)
    return render_template("user.html", user=response)

@user_bp.route('/user/mypage/info')
def get_info():
    user_id = request.headers.get("user_id")
    user = UserService.get_user(user_id)

    response: PexDTO.Response.DetailedUser = PexDTO.Response.DetailedUser(
        user_id=user.id,
        username=user.name,
        age=user.age,
        major=user.major,
        university=user.university,
        university_status=user.university_status,
        grade=user.grade,
        address=user.address,
        detail_address=user.detail_address,
        email=user.email,
        phone_number=user.phone_number,
        profile_path=user.profile_path,
        work_experiences=[
            PexDTO.Response.WorkExperience(
                work_experience_id=exp.work_experience_id,
                from_date=exp.from_date,
                to_date=exp.to_date,
                company_name=exp.company_name,
                position=exp.position,
                responsibility=exp.responsibility
            )
            for exp in user.work_experiences
        ],
        project_experiences=[
            PexDTO.Response.ProjectExperience(
                project_experience_id=proj.project_experience_id,
                project_name=proj.project_name,
                from_date=proj.from_date,
                to_date=proj.to_date,
                contents=[
                    PexDTO.Response.ProjectExperienceContent(
                        project_experience_task_id=task.project_experience_task_id,
                        content=task.content
                    )
                    for task in proj.contents
                ]
            )
            for proj in user.project_experiences
        ]
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@user_bp.route('/user/profile')
def get_profile():
    user_id = request.headers.get("user_id")
    user = UserService.get_user(user_id)

    response = {
        "profilePath": user.profile_path
    }

    json_response = json.dumps(response, ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@user_bp.route('/user/mypage/resume')
def get_resumes():
    user_id = request.headers.get("user_id")
    page, count = get_pagination_params()

    user = UserService.get_user(user_id)
    resumes, total = ResumeService.get_resumes(user_id, page, count)

    response = {
        "user": {
            "userId": user.id,
            "username": user.name,
            "profilePath": user.profile_path
        },
        "resumes": [
            {
                "resumeId": resume.resume_id,
                "title": resume.title,
                "viewCount": resume.view_count,
                "likeCount": resume.like_count,
                "occupation": {
                    "occupationId": resume.occupation_id,
                    "occupationName": resume.occupation_name
                },
                "job": resume.job,
                "level": resume.level,
                "createdTime": resume.created_time
            }
            for resume in resumes
        ],
        "total": total
    }

    json_response = json.dumps(response, ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@user_bp.route('/user/mypage/interview')
def get_interviews():
    user_id = request.headers.get("user_id")
    page, count = get_pagination_params()

    user = UserService.get_user(user_id)
    interviews, total = InterviewService.get_interviews(user_id, page, count)

    response = {
        "user": {
            "userId": user.id,
            "username": user.name,
            "profilePath": user.profile_path
        },
        "interviews": [
            {
                "interviewId": interview.interview_id,
                "title": interview.title,
                "isPublic": interview.is_public,
                "viewCount": interview.view_count,
                "likeCount": interview.like_count,
                "occupation": {
                    "occupationId": interview.occupation_id,
                    "occupationName": interview.occupation_name
                },
                "job": interview.job,
                "level": interview.level,
                "createdTime": interview.created_time
            }
            for interview in interviews
        ],
        "total": total
    }

    json_response = json.dumps(response, ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@user_bp.route('/user/requirements', methods=['POST'])
def create_requirements():
    user_id = request.headers.get("user_id")  # 토큰에서 user_id 추출

    # 요청 바디에서 데이터를 추출합니다.
    data = request.get_json()
    keywords = data.get("keywords", [])
    job_id = data.get("jobId")
    level = data.get("level")
    pros = data.get("pros")
    cons = data.get("cons")
    prompt = data.get("prompt", "")  # 선택 필드
    title = data.get("title", [])  # 선택 필드

    # 필수 값 확인
    if not keywords or job_id is None or not level or not pros or not cons:
        return Response(json.dumps({"error": "필수 필드가 누락되었습니다."}), status=400, content_type='application/json; charset=utf-8')

    # 데이터베이스에 저장하는 서비스 계층 호출
    RequirementsService.create_requirements(user_id, keywords, job_id, level, pros, cons, prompt, title)

    # 응답 생성
    return Response(status=201)

@user_bp.route('/user/necessary', methods=['POST'])
def register_necessary_info():
    # 헤더에서 ACCESS TOKEN을 통해 사용자 ID를 추출
    user_id = request.headers.get("user_id")

    # 요청 바디에서 필수 정보 데이터를 추출합니다.
    data = request.get_json()
    name = data.get("name")
    age = data.get("age")
    email = data.get("email")
    address = data.get("address")
    detail_address = data.get("detailAddress")

    # 필수 필드 유효성 검사를 수행합니다.
    if not all([name, age, email, address]):
        return Response(json.dumps({"error": "필수 필드가 누락되었습니다."}), status=400, content_type='application/json; charset=utf-8')

    # 데이터베이스에 저장하기 위해 서비스 계층을 호출합니다.
    NecessaryInfoService.register_info(user_id, name, age, email, address, detail_address)

    # 응답: 성공 시 204 No Content를 반환
    return Response(status=204)

@user_bp.route('/user/optional', methods=['POST'])
def register_optional_info():
    # 헤더에서 ACCESS TOKEN을 통해 사용자 ID를 추출
    user_id = request.headers.get("user_id")

    # 요청 바디에서 선택 정보 데이터를 추출합니다.
    data = request.get_json()
    major = data.get("major")
    university = data.get("university")
    university_status = data.get("universityStatus")
    grade = data.get("grade")
    project_experiences = data.get("projectExperiences", [])
    work_experiences = data.get("workExperiences", [])
    phone_number = data.get("phoneNumber")

    # 데이터베이스에 저장하기 위해 서비스 계층을 호출합니다.
    OptionalInfoService.register_info(
        user_id=user_id,
        major=major,
        university=university,
        university_status=university_status,
        grade=grade,
        project_experiences=project_experiences,
        work_experiences=work_experiences,
        phone_number=phone_number
    )

    # 응답: 성공 시 201 Created를 반환
    return Response(status=201)


@user_bp.route('/user/verify/send', methods=['POST'])
def send_verification_code():
    # 요청 바디에서 이메일 주소를 추출합니다.
    data = request.get_json()
    email = data.get("email")

    # 필수 값 확인
    if not email:
        return Response(json.dumps({"error": "이메일은 필수 항목입니다."}), status=400, content_type='application/json; charset=utf-8')

    # 서비스 계층에서 이메일 인증 코드 발송을 처리
    VerificationService.send_verification_code(email)

    # 성공 시 204 No Content 반환
    return Response(status=204)

@user_bp.route('/user/verify/compare', methods=['POST'])
def verify_code():
    # 요청 바디에서 이메일 주소와 인증 코드를 추출합니다.
    data = request.get_json()
    email = data.get("email")
    verify_code = data.get("verifyCode")

    # 필수 값 확인
    if not email or not verify_code:
        return Response(json.dumps({"error": "이메일과 인증 코드는 필수 항목입니다."}), status=400, content_type='application/json; charset=utf-8')


    is_valid = VerificationService.verify_code(email, verify_code) # 서비스 계층에서 이메일 인증 코드 검증을 처리

    if is_valid:

        return Response(status=204) # 인증 성공 시 204 No Content 반환
    else:
        # 인증 실패 시 400 Bad Request 반환
        return Response(json.dumps({"error": "잘못된 인증 코드입니다."}), status=400, content_type='application/json; charset=utf-8')

@user_bp.route('/user/profile', methods=['PATCH'])
def update_profile_picture():
    # 인증 토큰에서 사용자 ID 추출 (토큰 인증 방식에 따라 수정 가능)
    user_id = request.headers.get("Authorization")  # 실제로는 토큰에서 사용자 ID 추출이 필요할 수 있음

    # 요청 파일에서 프로필 이미지 파일 가져오기
    if 'profile' not in request.files:
        return Response(json.dumps({"error": "프로필 파일이 필요합니다."}), status=400, content_type='application/json; charset=utf-8')

    file = request.files['profile']
    if file.filename == '':
        return Response(json.dumps({"error": "유효한 파일이 필요합니다."}), status=400, content_type='application/json; charset=utf-8')

    # 파일명을 안전하게 처리하고, 파일 확장자 검증 (이미지 파일인지 확인)
    filename = secure_filename(file.filename)
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return Response(json.dumps({"error": "지원되지 않는 파일 형식입니다."}), status=400, content_type='application/json; charset=utf-8')

    # 파일 저장 경로 설정
    upload_folder = current_app.config['UPLOAD_FOLDER']  # 업로드 폴더는 config에 정의되어 있어야 함
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # 데이터베이스의 프로필 경로 업데이트
    UserService.update_profile_picture(user_id, file_path)

    # 성공 시 204 No Content 반환
    return Response(status=204)

from flask import Blueprint, request, Response, json
from services.user_service import UserService

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['DELETE'])
def delete_user():

    user_id = request.headers.get("Authorization")

    # 필수 값 확인
    if not user_id:
        return Response(json.dumps({"error": "사용자 ID가 필요합니다."}), status=400, content_type='application/json; charset=utf-8')

    # 서비스 계층에서 사용자 삭제 처리
    try:
        UserService.delete_user(user_id)
    except Exception as e:
        return Response(json.dumps({"error": "사용자 삭제 중 오류가 발생했습니다."}), status=500, content_type='application/json; charset=utf-8')

    # 성공 시 204 No Content 반환
    return Response(status=204)


@user_bp.route('/user/logout', methods=['POST'])
def logout():
    redirect_uri = request.args.get('redirect_uri')
    if redirect_uri is None:
        redirect_uri = request.headers.get('Referer') or 'http://localhost:5000/'

    response = make_response(redirect(redirect_uri))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        jwt_factory = JWTFactory()
        jwt_factory.delete_refresh_token(refresh_token)

    return response
