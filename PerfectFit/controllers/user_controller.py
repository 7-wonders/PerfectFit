from dataclasses import asdict
import json
from flask import Blueprint, render_template, request, Response

from dto.ProjectExperience.projectExperience import PexDTO
from dto.user.user import UserDto
from services.user_service import UserService

user_bp = Blueprint('user', __name__)

@user_bp.route('/users')
def get_users():
    page = request.args.get('page', default=1, type=int) # 현재 페이지 번호. 기본값은 1
    count = request.args.get('count', default=10, type=int) # 한 페이지에 보여줄 사용자 수. 기본값은 10

    paginate_user = UserService.get_users(page, count) #서비스 계층에서 사용자 목록을 가져옵니다. 페이지와 사용자 수를 기준으로 데이터베이스에서 사용자 정보를 읽어옵니다.
    response: UserDto.Response.Users = UserDto.Response.Users( #사용자의 정보를 UserDto 데이터 구조에 맞게 변환하여 users와 pages 필드에 담습니다.
        users=[UserDto.Response.IntroUser(user.user_id, user.username) for user in paginate_user.items],
        pages=paginate_user.pages,
    )

    return render_template("users.html", users=asdict(response))
    # 데이터베이스에서 가져온 사용자 목록을 users.html 템플릿에 전달하여 사용자 목록을 렌더링합니다. asdict를 통해 데이터를 딕셔너리 형태로 변환합니다.

@user_bp.route('/user/<user_id>')
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    response: UserDto.Response.IntroUser = UserDto.Response.IntroUser(user.id, user.name)

    return render_template("user.html", user=response)

@user_bp.route('/user/mypage/info')
def get_info(user_id: int):
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

    user_id = request.headers.get("user_id")  # 토큰에서 user_id를 가져오는 코드입니다!

    user = UserService.get_user(user_id)

    response = {
        "profilePath": user.profile_path # Response입니다.
    }

    json_response = json.dumps(response, ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')