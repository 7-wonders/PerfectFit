import os
from http import HTTPStatus

from flask import Blueprint, render_template, request, redirect, session, make_response, Response, url_for

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from services.auth_service import AuthService
from utils.cookie import Cookie
from utils.oauth.google_oauth_handler import GoogleOAuthHandler
from utils.oauth.kakao_oauth_handler import KakaoOAuthHandler
from utils.oauth.naver_oauth_handler import NaverOAuthHandler

auth_bp = Blueprint('auth', __name__)

logger = Logger('auth_controller')
env = os.getenv('FLASK_ENV')

if env == 'development':
    domain = 'localhost'
else:
    domain = os.getenv('PRODUCTION_URL')


def _create_response(token_info: dict, redirect_uri: str | None) -> Response:
    if redirect_uri:
        response = make_response(redirect(redirect_uri))
    else:
        response = make_response()

    Cookie.save(response, 'access_token', token_info['access_token'], token_info['access_token_exp'])
    Cookie.save(response, 'refresh_token', token_info['refresh_token'], token_info['refresh_token_exp'])

    return response


@auth_bp.route('/login/google', methods=['GET'])
def login_google():
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'
    return redirect(GoogleOAuthHandler().get_login_url())


@auth_bp.route('/google', methods=['GET'])
def auth_google_callback():
    code = request.args.get('code', type=str)
    error = request.args.get('error', type=str)
    redirect_uri = session.get('redirect_uri') or 'http://localhost:5000/'

    if error == 'access_denied':
        return redirect(redirect_uri)

    if not code or error:
        raise CustomException(ExceptionType.GOOGLE_LOGIN_ERROR)

    response, isExists = AuthService.google_login(code)

    if isExists:
        session.pop('redirect_uri', None)
        return _create_response(response, redirect_uri)
    else:
        session['user_info'] = response
        return redirect(url_for('user.register_necessary_info'))


@auth_bp.route('/login/naver', methods=['GET'])
def auth_naver():
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'
    return redirect(NaverOAuthHandler().get_login_url())


@auth_bp.route('/naver', methods=['GET'])
def auth_naver_callback():
    code = request.args.get('code', type=str)
    state = request.args.get('state', type=str)
    redirect_uri = session.get('redirect_uri') or 'http://localhost:5000/'

    if not code or not state:
        raise CustomException(ExceptionType.NAVER_LOGIN_ERROR)

    response, isExists = AuthService.naver_login(code, state)

    if isExists:
        session.pop('redirect_uri', None)
        return _create_response(response, redirect_uri)
    else:
        session['user_info'] = response
        return redirect(url_for('user.register_necessary_info'))


@auth_bp.route('/login/kakao', methods=['GET'])
def auth_kakao():
    session['redirect_uri'] = request.args.get('redirect_uri', type=str) or 'http://localhost:5000/'
    return redirect(KakaoOAuthHandler().get_login_url())


@auth_bp.route('/kakao', methods=['GET'])
def auth_kakao_callback():
    code = request.args.get('code', type=str)
    error = request.args.get('error', type=str)
    state = request.args.get('state', type=str)

    redirect_uri = session.get('redirect_uri') or 'http://localhost:5000/'

    if error == 'access_denied':
        return redirect(redirect_uri)

    if not code or error:
        raise CustomException(ExceptionType.KAKAO_LOGIN_ERROR)

    response, isExists = AuthService.kakao_login(code, state)

    if isExists:
        session.pop('redirect_uri', None)
        return _create_response(response, redirect_uri)
    else:
        session['user_info'] = response
        return redirect(url_for('user.register_necessary_info'))


@auth_bp.route('/', methods=['POST'])
def renew_token():
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        raise CustomException(ExceptionType.INVALID_TOKEN)

    token_info = AuthService.renew_token(refresh_token)

    response = _create_response(token_info, None)
    response.status_code = HTTPStatus.NO_CONTENT

    return response
