import os
from urllib.parse import quote

from flask import Blueprint, render_template, request, url_for, redirect, session

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

logger = Logger('auth_controller')


@auth_bp.route('/test')
def test():
    return render_template('test.html')


@auth_bp.route('/auth/login/google', methods=['GET'])
def login_google():
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'

    if not client_id or not redirect_uri:
        logger.error(f"Google Environment Error\n"
                     f"client_id : {client_id} | redirect_uri : {redirect_uri}")
        raise CustomException(ExceptionType.GOOGLE_ENVIRONMENT_ERROR)

    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email profile")


@auth_bp.route('/auth/google', methods=['GET'])
def auth_google():
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
