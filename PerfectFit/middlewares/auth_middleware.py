from flask import request

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType

auth_required_routes = {
    # 'URL명': ['HTTP 메소드1', 'HTTP 메소드2', ...],
}


def is_authentication_required():
    path = request.path
    method = request.method

    return path in auth_required_routes and method in auth_required_routes[path]


def authenticate_request():
    if is_authentication_required():
        access_token = request.cookies.get('access_token')

        if not access_token:
            raise CustomException(ExceptionType.INVALID_TOKEN)
