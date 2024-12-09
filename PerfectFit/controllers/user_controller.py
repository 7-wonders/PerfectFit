import os
from dataclasses import asdict
import json
from flask import current_app, Response, request, session
from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, redirect, make_response

from controllers.auth_controller import _create_response
from dto.user.user import UserDto
from services.auth_service import AuthService
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

    return render_template("testusers.html", response=asdict(response))


@user_bp.route('/user/<user_id>')
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    response: UserDto.Response.IntroUser = UserDto.Response.IntroUser(user.user_id, user.username)
    return render_template("testusers.html", response=response)


@user_bp.route('/user/mypage/information')
def get_info():
    response = UserService.get_information()
    return render_template("mypage_information.html", response=response)


@user_bp.route('/user/profile')
def get_profile():
    user = UserService.get_user()

    response = {
        "profilePath": user.profile_path
    }

    return Response(
        json.dumps(response, ensure_ascii=False, indent=2),  ##  한글이 깨지지 않도록 처리하였습니다!
        status=200,
        content_type='application/json; charset=utf-8'
    )


@user_bp.route('/user/mypage/resume')
def get_resumes():
    page, count = get_pagination_params()

    response = UserService.get_user_with_resumes(page, count)
    return render_template("mypage_resume.html", response=response)


@user_bp.route('/user/mypage/interview')
def get_interviews():
    page, count = get_pagination_params()
    response = UserService.get_my_interviews(page, count)

    return render_template("mypage_interview.html", response=response)


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
    redis_instance = Redis()
    redis_key = f"user:{user_id}:requirements"
    redis_value = json.dumps(data, ensure_ascii=False)

    redis_instance.save(redis_key, redis_value)

    # 리다이렉션으로 응답 반환
    return redirect("/requirements/success")


@user_bp.route('/user/necessary', methods=['GET', 'POST'])
def register_necessary_info():
    if request.method == 'GET':
        is_login = bool(request.cookies.get('access_token')) or bool(session.get('user_info'))

        if session.get('user_info'):
            user_info: UserDto.Request.Signup = session.get('user_info')

            return render_template("information_required.html", response={
                "username": user_info['username'],
                "age": user_info['age'] if user_info['age'] else '',
                "email": user_info['email'] if user_info['email'] else '',
                "isLogin": is_login
            })
        else:
            response = NecessaryInfoService.get_info()
            return render_template("information_required.html", response={
                "username": response.username,
                "age": response.age,
                "email": response.email,
                "address": response.address,
                "detailAddress": response.detailAddress,
                "isLogin": is_login
            })
    else:
        # 요청 바디에서 필수 정보 데이터를 추출합니다.
        name = request.form.get("name")
        age = int(request.form.get("age"))
        email_local = request.form.get("email", "")  # 기본값을 ""로 설정
        email_domain = request.form.get("emailDomain", "")  # 기본값을 ""로 설정
        email = email_local + email_domain
        address = request.form.get("address")
        detail_address = request.form.get("detailAddress")

        # 데이터베이스에 저장하기 위해 서비스 계층을 호출합니다.
        if session.get('user_info'):
            session_data = session.get('user_info')
            data = {
                "snsId": session_data['snsId'],
                "snsKind": session_data['snsKind'],
                "profilePath": session_data['profilePath'],
                "username": name,
                "age": age,
                "email": email,
                "address": address,
                "detailAddress": detail_address,
            }
            session['user_info'] = data

            return redirect("/user/optional")
        else:
            user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))
            NecessaryInfoService.register_info(user_id, name, age, email, address, detail_address)

            # 응답: 성공 시 204 No Content를 반환
            return redirect(f"/user/mypage/information")


@user_bp.route('/user/optional', methods=['GET', 'POST'])
def register_optional_info():
    if request.method == 'GET':
        if session.get('user_info'):
            user_info: UserDto.Response.NecessaryInfo = session.get('user_info')
            return render_template("information_selected.html", response={
                "username": user_info['username'],
                "age": user_info['age'],
                "email": user_info['email'],
                "address": user_info['address'],
                "detailAddress": user_info['detailAddress'],
            })
        else:
            response = NecessaryInfoService.get_optional_info()
            return render_template("information_selected.html", response=response)
    else:
        major = request.form.get("major")  # 전공
        university = request.form.get("university")
        university_status = request.form.get("universityStatus")
        grade = request.form.get("grade")  # 학점
        phone_number = request.form.get("phoneNumber")

        project_experiences = []
        index = 0

        while True:
            project_name = request.form.get(f"projectExperiences[{index}][projectName]")
            from_date = request.form.get(f"projectExperiences[{index}][fromDate]")
            to_date = request.form.get(f"projectExperiences[{index}][toDate]")
            contents = request.form.getlist(f"projectExperiences[{index}][contents]")

            if not project_name:
                break

            project_experiences.append({
                "projectName": project_name,
                "fromDate": from_date,
                "toDate": to_date,
                "contents": contents
            })
            index += 1
        work_experiences = []
        index = 0

        while True:
            company_name = request.form.get(f"workExperiences[{index}][company_name]")
            from_date = request.form.get(f"workExperiences[{index}][fromDate]")
            to_date = request.form.get(f"workExperiences[{index}][toDate]")
            position = request.form.get(f"workExperiences[{index}][position]")
            responsibility = request.form.get(f"workExperiences[{index}][responsibility]")
            reason = request.form.get(f"workExperiences[{index}][reason]")

            if not company_name:
                break

            work_experiences.append({
                "companyName": company_name,
                "fromDate": from_date,
                "toDate": to_date,
                "position": position,
                "responsibility": responsibility,
                "reason": reason
            })
            index += 1

        if session.get('user_info'):
            user_info: UserDto.Response.NecessaryInfo = session.get('user_info')
            token_info = AuthService.signup(
                major=major,
                university=university,
                university_status=university_status,
                grade=grade,
                phone_number=phone_number,
                project_experiences=project_experiences,
                work_experiences=work_experiences,
                info=user_info,
            )

            redirect_uri = session.get('redirect_uri') or 'http://127.0.0.1:5000/'
            session.pop('redirect_uri', None)
            session.pop('user_info', None)

            return _create_response(token_info, redirect_uri)
        else:
            user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))
            OptionalInfoService.register_info(
                user_id=user_id,
                major=major,
                university=university,
                university_status=university_status,
                grade=grade,
                phone_number=phone_number
            )

            OptionalInfoService.register_projectexp(
                user_id=user_id,
                project_experiences=project_experiences,
            )

            OptionalInfoService.register_workexp(
                user_id=user_id,
                work_experiences=work_experiences,
            )

            redirect_uri = "/user/mypage/information"
            return redirect(redirect_uri)


@user_bp.route('/user/verify/send', methods=['POST'])
def send_verification_code():
    # 요청 바디에서 이메일 주소를 추출합니다.
    data = request.get_json()
    email = data.get("email")
    # 필수 값 확인
    if not email:
        return Response(json.dumps({"error": "이메일은 필수 항목입니다."}), status=400,
                        content_type='application/json; charset=utf-8')

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
        return Response(json.dumps({"error": "이메일과 인증 코드는 필수 항목입니다."}), status=400,
                        content_type='application/json; charset=utf-8')

    is_valid = VerificationService.verify_code(email, verify_code)  # 서비스 계층에서 이메일 인증 코드 검증을 처리

    if is_valid:

        return Response(status=204)  # 인증 성공 시 204 No Content 반환
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
        return Response(json.dumps({"error": "사용자 ID가 필요합니다."}), status=400,
                        content_type='application/json; charset=utf-8')

    # 서비스 계층에서 사용자 삭제 처리
    try:
        UserService.delete_user(user_id)
    except Exception as e:
        return Response(json.dumps({"error": "사용자 삭제 중 오류가 발생했습니다."}), status=500,
                        content_type='application/json; charset=utf-8')

    # 성공 시 204 No Content 반환
    return Response(status=204)


@user_bp.route('/user/logout', methods=['POST'])
def logout():
    redirect_uri = request.args.get('redirect_uri')
    if redirect_uri is None:
        redirect_uri = request.headers.get('Referer') or 'http://127.0.0.1:5000/'

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

@user_bp.route('/user/test/selected')
def get_mypage_selected():
    return render_template("information_selected.html")
