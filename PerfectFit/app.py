from flask import Flask, render_template, request, url_for, send_from_directory
from dotenv import load_dotenv

from database.config import Config, db  # Config와 db를 import
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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(CustomException)
def custom_exception(e: CustomException):
    logger.error(e.__str__())

    if is_api_call(request):
        response = e.__to_json__()
        response.status_code = e.exception.status_code
        return response
    else:
        return render_template("error_page.html", error=e), e.exception.status_code


@app.errorhandler(Exception)
def internal_server_error_page(e: Exception):
    # Log로 변경 해야함.
    print("Error : ", e.__str__())

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
