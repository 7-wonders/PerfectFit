from flask import Blueprint, render_template, request, url_for, redirect

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

logger = Logger('auth_controller')


@auth_bp.route('/test')
def test():
    return render_template('test.html')


@auth_bp.route('/auth/google')
def auth_google():
    code = request.args.get('code', type=str)
    error = request.args.get('error', type=str)

    if code:
        logger.info(f'Code : {code}')

    if error == 'access_denied':
        return redirect(url_for('index'))

    if error:
        raise CustomException(ExceptionType.GOOGLE_LOGIN_ERROR)

    AuthService.google_login(code)

    return redirect(url_for('index'))
