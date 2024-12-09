import re

from flask import request, make_response, redirect

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from utils.cookie import Cookie
from utils.jwt_factory import JWTFactory

auth_required_routes = {
    # 'URL명': ['HTTP 메소드1', 'HTTP 메소드2', ...],
    '/resume': ['POST'],
    '/resume/waiting': ['GET'],
    '/resume/write': ['GET', 'POST'],
    '/resume/information': ['GET', 'POST'],
    r'^/resume/\d+/update$': ['GET', 'POST'],
}

jwt_factory = JWTFactory()


def is_authentication_required():
    path = request.path
    method = request.method

    for route, methods in auth_required_routes.items():
        if route.startswith('^'):
            if re.match(route, path):
                return method in methods
        else:
            if route == path:
                return method in methods

    return False


def authenticate_request():
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')

    if is_authentication_required():
        if not access_token:
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
    else:
        if not access_token and refresh_token:
            token_info = jwt_factory.renew_token(refresh_token)
            jwt_factory.delete_refresh_token(refresh_token)
            jwt_factory.verify_access_token(token_info['access_token'])

            response = make_response(redirect(request.url))
            Cookie.save(response, 'access_token', token_info['access_token'], token_info['access_token_exp'])
            Cookie.save(response, 'refresh_token', token_info['refresh_token'], token_info['refresh_token_exp'])

            return response
