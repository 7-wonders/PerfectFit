from dataclasses import asdict

from flask import Blueprint, render_template, request

from dto.user.user import UserDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from services.user_service import UserService
from utils.const import const

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['POST'])
def post_user():
    user_data = request.get_json()

    if 'snsKind' not in user_data:
        raise CustomException(ExceptionType.REQUIRED_SNS_KIND)
    if 'snsId' not in user_data:
        raise CustomException(ExceptionType.REQUIRED_SNS_ID)
    if 'name' not in user_data:
        raise CustomException(ExceptionType.REQUIRED_NAME)

    if user_data['snsKind'] not in const.valid_sns_kinds:
        raise CustomException(ExceptionType.SNS_KIND_BAD_REQUEST)
    if len(user_data['name']) > 32:
        raise CustomException(ExceptionType.NAME_BAD_REQUEST)

    #jwt_token = UserService.post_user(user_data)
    jwt_token = "tokenstokens"

    return {"token": jwt_token}, 201


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
