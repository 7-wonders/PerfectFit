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
        users=[UserDto.Response.IntroUser(user.id, user.name) for user in paginate_user.items],
        pages=paginate_user.pages,
    )

    return render_template("users.html", users=asdict(response))


@user_bp.route('/user/<user_id>')
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        return render_template("user.html")

    response: UserDto.Response.IntroUser = UserDto.Response.IntroUser(user.id, user.name)

    return render_template("user.html", user=response)

@user_bp.route('/user/mypage/resume')
def get_mypage_resume():
    return render_template("mypage_resume.html", active_page = 'resume')

@user_bp.route('/user/mypage/interview')
def get_mypage_interview():
    return render_template("mypage_interview.html", active_page = 'interview')

@user_bp.route('/user/mypage/information')
def get_mypage_information():
    return render_template("mypage_information.html", active_page = 'information')

@user_bp.route('/user/resume/write/part')
def get_resume_write_part():
    return render_template("resume_write_part.html")

@user_bp.route('/user/resume/write/all')
def get_resume_write_all():
    return render_template("resume_write_all.html")

@user_bp.route('/user/resume/select')
def get_resume_select():
    return render_template("resume_select.html")

@user_bp.route('/user/resume/information/all')
def get_resume_information_all():
    return render_template("resume_information_all.html")

@user_bp.route('/user/resume/information/part')
def get_resume_information_part():
    return render_template("resume_information_part.html")

@user_bp.route('/user/resume/loading')
def get_resume_load_loading():
    return render_template("resume_loading.html")