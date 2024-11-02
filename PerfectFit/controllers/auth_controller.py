import os

from flask import Blueprint, render_template, request, redirect, session

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from services.auth_service import AuthService
from utils.oauth.google_oauth_handler import GoogleOAuthHandler
from utils.oauth.kakao_oauth_handler import KakaoOAuthHandler
from utils.oauth.naver_oauth_handler import NaverOAuthHandler

auth_bp = Blueprint('auth', __name__)

logger = Logger('auth_controller')


@auth_bp.route('/test', methods=['GET'])
def test():
    return render_template("test.html")


@auth_bp.route('/login/google', methods=['GET'])
def login_google():
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'
    return redirect(GoogleOAuthHandler().get_login_url())


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
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'
    return redirect(NaverOAuthHandler().get_login_url())


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


@auth_bp.route('/login/kakao', methods=['GET'])
def auth_kakao():
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'
    return redirect(KakaoOAuthHandler().get_login_url())


@auth_bp.route('/kakao', methods=['GET'])
def auth_kakao_callback():
    code = request.args.get('code', type=str)
    error = request.args.get('error', type=str)
    state = request.args.get('state', type=str)

    redirect_uri = session.get('redirect_uri')
    session.pop('redirect_uri', None)

    if error == 'access_denied':
        return redirect(redirect_uri)

    if not code or error:
        raise CustomException(ExceptionType.KAKAO_LOGIN_ERROR)

    AuthService.kakao_login(code, state)

    return redirect(redirect_uri)
