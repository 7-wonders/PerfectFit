from dataclasses import asdict

from flask import Blueprint, render_template, request

from dto.user.user import UserDto
from services.user_service import UserService

user_bp = Blueprint('user', __name__)


@user_bp.route('/users')
def get_users():
    page = request.args.get('page', default=1, type=int)
    count = request.args.get('count', default=10, type=int)

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