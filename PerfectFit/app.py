from flask import Flask, render_template, request, url_for, send_from_directory, make_response, redirect, Response
from dotenv import load_dotenv

from config.config_mysql import Config, db  # Config와 db를 import
from controllers.user_controller import user_bp
from controllers.auth_controller import auth_bp

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from utils.check_api import is_api_call

load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)  # config.py의 Config 클래스를 사용

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")

# 데이터베이스 초기화
db.init_app(app)

logger = Logger("exception")


def _delete_cookie(response: Response) -> Response:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(CustomException)
def custom_exception(e: CustomException):
    logger.error(e.__str__())

    if e.exception.value == ExceptionType.INVALID_TOKEN.value or e.exception.value == ExceptionType.EXPIRED_TOKEN.value:
        if is_api_call(request):
            response = e.__to_json__()
            response.status_code = e.exception.status_code
            return _delete_cookie(response)

        if request.url == url_for("auth.renew_token", _external=True):
            previous_url = request.headers.get("Referer")
            response = make_response(redirect("http://localhost:5000/login?redirect_uri=" + previous_url))
            return _delete_cookie(response)

        response = make_response(redirect("http://localhost:5000/login?redirect_uri=" + request.url))
        return _delete_cookie(response)

    if is_api_call(request):
        response = e.__to_json__()
        response.status_code = e.exception.status_code
        return response
    else:
        return render_template("error_page.html", error=e), e.exception.status_code


@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html", error=e), 404


@app.errorhandler(Exception)
def internal_server_error_page(e: Exception):
    logger.error(e.__str__())

    exception = CustomException(ExceptionType.INTERNAL_SERVER_ERROR)

    if is_api_call(request):
        response = exception.__to_json__()
        response.status_code = exception.exception.status_code
        return response
    else:
        return render_template("error_page.html", error=exception), 500


@app.route('/')
def index():
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
