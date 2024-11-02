import os

from flask import Blueprint, render_template, request, redirect, session

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

logger = Logger('auth_controller')


@auth_bp.route('/test', methods=['GET'])
def test():
    return render_template("test.html")


@auth_bp.route('/login/google', methods=['GET'])
def login_google():
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'

    if not client_id or not redirect_uri:
        logger.error(f"Google Environment Error\n"
                     f"client_id : {client_id} | redirect_uri : {redirect_uri}")
        raise CustomException(ExceptionType.GOOGLE_ENVIRONMENT_ERROR)

    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email profile")


@auth_bp.route('/google', methods=['GET'])
def auth_google_callback():
    code = request.args.get('code', type=str)
    error = request.args.get('error', type=str)
    redirect_uri = session.get('redirect_uri')
    session.pop('redirect_uri', None)

    if error == 'access_denied':
        return redirect(redirect_uri)

    if not code or error:
        raise CustomException(ExceptionType.GOOGLE_LOGIN_ERROR)

    AuthService.google_login(code)

    return redirect(redirect_uri)


@auth_bp.route('/login/naver', methods=['GET'])
def auth_naver():
    client_id = os.environ.get('NAVER_CLIENT_ID')
    redirect_uri = os.environ.get('NAVER_REDIRECT_URI')
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'

    if not client_id or not redirect_uri:
        logger.error(f"Naver Environment Error\n"
                     f"client_id : {client_id} | redirect_uri : {redirect_uri}")
        raise CustomException(ExceptionType.NAVER_ENVIRONMENT_ERROR)

    return redirect(f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state=STATE")


@auth_bp.route('/naver', methods=['GET'])
def auth_naver_callback():
    code = request.args.get('code', type=str)
    state = request.args.get('state', type=str)
    redirect_uri = session.get('redirect_uri')
    session.pop('redirect_uri', None)

    if not code or not state:
        raise CustomException(ExceptionType.NAVER_LOGIN_ERROR)

    AuthService.naver_login(code, state)

    return redirect(redirect_uri)
