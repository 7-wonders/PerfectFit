from flask import request, Response, url_for, redirect, make_response, render_template, Blueprint
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from utils.check_api import is_api_call

logger = Logger("exception")
eh_bp = Blueprint("exception_handler", __name__)


def delete_cookie(response: Response) -> Response:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@eh_bp.app_errorhandler(CustomException)
def custom_exception(e: CustomException):
    logger.error(e.__str__())

    if e.exception.value == ExceptionType.INVALID_TOKEN.value or e.exception.value == ExceptionType.EXPIRED_TOKEN.value:
        print("=========================================")
        print(request)
        print(is_api_call(request))
        print(request.content_type)
        print(request.accept_mimetypes)
        print("=========================================")

        if is_api_call(request):
            response = e.__to_json__()
            response.status_code = e.exception.status_code
            return delete_cookie(response)

        if request.url == url_for("auth.renew_token", _external=True):
            previous_url = request.headers.get("Referer")

            # 호스팅 시 주소 변경 필요
            if previous_url is None or 'localhost' not in previous_url:
                previous_url = "http://localhost:5000/"

            response = make_response(redirect("http://localhost:5000/login?redirect_uri=" + previous_url))
            return delete_cookie(response)

        response = make_response(redirect("http://localhost:5000/login?redirect_uri=" + request.url))
        return delete_cookie(response)

    if is_api_call(request):
        response = e.__to_json__()
        response.status_code = e.exception.status_code
        return response
    else:
        return render_template("error_page.html", error=e), e.exception.status_code


@eh_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html", error=e), 404


@eh_bp.app_errorhandler(Exception)
def internal_server_error_page(e: Exception):
    logger.error(e.__str__())

    exception = CustomException(ExceptionType.INTERNAL_SERVER_ERROR)

    if is_api_call(request):
        response = exception.__to_json__()
        response.status_code = exception.exception.status_code
        return response
    else:
        return render_template("error_page.html", error=exception), 500
