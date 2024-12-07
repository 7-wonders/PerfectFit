import os
from dataclasses import asdict
import json
from flask import current_app, Response, request
from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, redirect, make_response

from dto.interview.interview import InterviewDto
from dto.occupation.occupation import OccupationDto
from dto.project_experience.project_experience import PexDTO
from dto.resume.resume import ResumeDto
from dto.user.user import UserDto
from dto.work_experience.work_experience import WorkExperienceDTO
from services.interview_service import InterviewService
from services.necessaryinfo_service import NecessaryInfoService
from services.optionalinfo_service import OptionalInfoService
from services.requirements_service import RequirementsService
from services.user_service import UserService
from services.verification_service import VerificationService
from utils.jwt_factory import JWTFactory

user_bp = Blueprint('user', __name__)


def get_pagination_params():
    """공통적으로 페이지네이션 파라미터를 가져오는 함수"""
    page = request.args.get('page', default=1, type=int)
    count = request.args.get('count', default=10, type=int)
    return page, count


@user_bp.route('/users')
def get_users():
    page, count = get_pagination_params()  # 페이지네이션 파라미터 함수 사용 // 테스트3

    paginate_user = UserService.get_users(page, count)
    response: UserDto.Response.Users = UserDto.Response.Users(
        users=[UserDto.Response.IntroUser(user.user_id, user.username) for user in paginate_user.items],
        pages=paginate_user.pages,
    )

    return render_template("testusers.html", users=asdict(response))


@user_bp.route('/user/<user_id>')
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    response: UserDto.Response.IntroUser = UserDto.Response.IntroUser(user.user_id, user.username)
    return render_template("testusers.html", user=response)


@user_bp.route('/user/mypage/info')
def get_info():
    # try:
    #     # 말씀하신 jwt 토큰 방식으로 변경하였습니다!
    #     access_token = request.cookies.get('access_token')
    #     jwt_factory = JWTFactory()
    #     user_id = jwt_factory.verify_access_token(access_token)
    # except ValueError as e:
    #     return Response(
    #         json.dumps({"error": str(e)}),
    #         status=401,
    #         content_type='application/json; charset=utf-8'
    #     )
    user = UserService.get_user()

    response = UserDto.Response.DetailedUser(
        user_id=user.user_id,
        username=user.username,
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
            WorkExperienceDTO.Response.WorkExperience(
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

    return render_template("testusers.html", user=asdict(response))  # JSON 데이터 전달


@user_bp.route('/user/profile')
def get_profile():
    user = UserService.get_user()

    response = {
        "profilePath": user.profile_path
    }

    json_response = json.dumps(response, ensure_ascii=False, indent=2)
    return render_template("testusers.html", user=response)


@user_bp.route('/user/mypage/resume')
def get_resumes():
    page, count = get_pagination_params()

    # get_user 하지말고 get_user with resumes 메소드를 만들어서 컨트롤러에 대응하는 서비스 만들고. user랑 resumes를 join시켰습니다
    user, resumes, total = UserService.get_user_with_resumes(page, count)

    # DTO를 사용하여 응답 생성
    response = ResumeDto.Response.MyResume(
        user=UserDto.Response.IntroUserWithProfile(
            userId=user.user_id,
            username=user.username,
            profilePath=user.profile_path
        ),
        resumes=[
            ResumeDto.Response.MyResumeInfo(
                resume_id=resume.resume_id,
                title=resume.title,
                # 컬럼에 view_count, like_count가 없어서 주석처리했습니다.
                # 직접 DB COUNT 해서 가져와야 합니다.
                # view_count=resume.view_count,
                # like_count=resume.like_count,
                view_count=1,
                like_count=1,
                occupation=OccupationDto.Response.Occupation(
                    # occupation 테이블을 통해서 가져와야 합니다.
                    # occupationId=resume.occupation_id,
                    # occupationName=resume.occupation_name
                    occupationId=1,
                    occupationName="Software Engineer"
                ),
                job=resume.job,
                level=resume.level,
                created_time=resume.created_time
            )
            for resume in resumes
        ],
        total=total
    )

    return render_template("testusers.html", user=response)


@user_bp.route('/user/mypage/interview')
def get_interviews():
    user_id = request.headers.get("user_id")
    page, count = get_pagination_params()

    # 사용자 및 인터뷰 데이터 조회
    user = UserService.get_user(user_id)
    interviews, total = InterviewService.get_interviews(user_id, page, count)

    # DTO를 사용하여 응답 생성
    response = InterviewDto.Response.IsPublicList(
        interviews=[
            InterviewDto.Response.IsPublicInterview(
                questionId=interview.question_id,
                title=interview.title,
                answer=interview.answer,
                isPublic=interview.is_public
            )
            for interview in interviews
        ]
    )

    return render_template("testusers.html", user=response)


@user_bp.route('/user/requirements', methods=['POST'])
def create_requirements():
    user_id = request.headers.get("user_id")  # 토큰에서 user_id 추출

    # 요청 데이터를 DTO로 변환
    data = request.get_json()
    request_dto = UserDto.Request.CreateRequirementsRequest(**data)  # **data로 전달

    # 필수 값 확인
    if not request_dto.keywords or request_dto.job_id is None or not request_dto.level or not request_dto.pros or not request_dto.cons:
        return Response(
            json.dumps({"error": "필수 필드가 누락되었습니다."}),
            status=400,
            content_type='application/json; charset=utf-8'
        )

    # 데이터베이스에 저장하는 서비스 계층 호출
    RequirementsService.create_requirements(
        user_id=user_id,
        keywords=request_dto.keywords,
        job_id=request_dto.job_id,
        level=request_dto.level,
        pros=request_dto.pros,
        cons=request_dto.cons,
        prompt=request_dto.prompt,
        title=request_dto.title
    )

    # Redis에 데이터 저장
    from config.config_redis import Redis
    redis_instance = Redis()  # Redis 인스턴스 생성
    redis_key = f"user:{user_id}:requirements"
    redis_value = json.dumps(data, ensure_ascii=False)

    redis_instance.save(redis_key, redis_value)

    # 리다이렉션으로 응답 반환
    return redirect("/requirements/success")

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
        return Response(json.dumps({"error": "필수 필드가 누락되었습니다."}), status=400,
                        content_type='application/json; charset=utf-8')

    # 데이터베이스에 저장하기 위해 서비스 계층을 호출합니다.
    NecessaryInfoService.register_info(user_id, name, age, email, address, detail_address)

    # 응답: 성공 시 204 No Content를 반환
    return Response(status=204)


@user_bp.route('/user/optional', methods=['POST'])
def register_optional_info():
    # 헤더에서 사용자 ID 추출
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

    # Redis에 저장할 데이터 생성
    redis_data = {
        "user_id": user_id,
        "major": major,
        "university": university,
        "university_status": university_status,
        "grade": grade,
        "project_experiences": project_experiences,
        "work_experiences": work_experiences,
        "phone_number": phone_number,
    }

    # Redis에 데이터 저장
    from config.config_redis import Redis
    redis_handler = Redis()
    redis_key = f"user:{user_id}:optional_info"
    redis_value = json.dumps(redis_data, ensure_ascii=False)

    redis_handler.save(redis_key, redis_value)

    # 데이터베이스에 저장하기 위해 서비스 계층 호출
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

    # 성공 시 리다이렉션
    redirect_uri = "/optional-info/success"
    return redirect(redirect_uri)


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
        return Response(json.dumps({"error": "잘못된 인증 코드입니다."}), status=400,
                        content_type='application/json; charset=utf-8')


@user_bp.route('/user/profile', methods=['PATCH'])
def update_profile_picture():
    # 인증 토큰에서 사용자 ID 추출 (토큰 인증 방식에 따라 수정 가능)
    user_id = request.headers.get("Authorization")  # 실제로는 토큰에서 사용자 ID 추출이 필요할 수 있음

    # 요청 파일에서 프로필 이미지 파일 가져오기
    if 'profile' not in request.files:
        return Response(json.dumps({"error": "프로필 파일이 필요합니다."}), status=400,
                        content_type='application/json; charset=utf-8')

    file = request.files['profile']
    if file.filename == '':
        return Response(json.dumps({"error": "유효한 파일이 필요합니다."}), status=400,
                        content_type='application/json; charset=utf-8')

    # 파일명을 안전하게 처리하고, 파일 확장자 검증 (이미지 파일인지 확인)
    filename = secure_filename(file.filename)
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return Response(json.dumps({"error": "지원되지 않는 파일 형식입니다."}), status=400,
                        content_type='application/json; charset=utf-8')

    # 파일 저장 경로 설정
    upload_folder = current_app.config['UPLOAD_FOLDER']  # 업로드 폴더는 config에 정의되어 있어야 함
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # 데이터베이스의 프로필 경로 업데이트
    UserService.update_profile_picture(user_id, file_path)

    # 성공 시 204 No Content 반환
    return Response(status=204)


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

# @user_bp.route('/user/mypage/resume')
# def get_mypage_resume():
#     return render_template("mypage_resume.html", active_page = 'resume')

# @user_bp.route('/user/mypage/interview')
# def get_mypage_interview():
#     return render_template("mypage_interview.html", active_page = 'interview')

# @user_bp.route('/user/mypage/information')
# def get_mypage_information():
#     return render_template("mypage_information.html", active_page = 'information')

