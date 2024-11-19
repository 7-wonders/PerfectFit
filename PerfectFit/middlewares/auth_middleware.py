from flask import request, make_response, redirect

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from utils.cookie import Cookie
from utils.jwt_factory import JWTFactory

auth_required_routes = {
    # 'URL명': ['HTTP 메소드1', 'HTTP 메소드2', ...],
    '/resume': ['POST'],
    '/resume/all': ['POST'],
    '/resume/write/all': ['GET'],
}

jwt_factory = JWTFactory()


def is_authentication_required():
    path = request.path
    method = request.method

    return path in auth_required_routes and method in auth_required_routes[path]


def authenticate_request():
    if is_authentication_required():
        access_token = request.cookies.get('access_token')

        if not access_token:
            refresh_token = request.cookies.get('refresh_token')

            if not refresh_token:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            token_info = jwt_factory.renew_token(refresh_token)
            jwt_factory.delete_refresh_token(refresh_token)
            jwt_factory.verify_access_token(token_info['access_token'])

            response = make_response(redirect(request.url))
            Cookie.save(response, 'access_token', token_info['access_token'], token_info['access_token_exp'])
            Cookie.save(response, 'refresh_token', token_info['refresh_token'], token_info['refresh_token_exp'])

            return response

        user_id = jwt_factory.verify_access_token(access_token)

        if not user_id:
            raise CustomException(ExceptionType.INVALID_TOKEN)
