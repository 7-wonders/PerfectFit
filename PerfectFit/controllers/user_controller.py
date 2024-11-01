from dataclasses import asdict

from flask import Blueprint, render_template, request

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


@user_bp.route('/user/<user_id>')
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    response: UserDto.Response.IntroUser = UserDto.Response.IntroUser(user.id, user.name)

    return render_template("user.html", user=response)

@user_bp.route('/user/mypage/info')
def get_info(user_id: int):
    user = UserService.get_user(user_id)


    ## 토큰 검사












