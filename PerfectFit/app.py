from flask import Flask, render_template, request

from database.config import Config, db  # Config와 db를 import
from controllers.user_controller import user_bp
from dotenv import load_dotenv

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from utils.check_api import is_api_call

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)  # config.py의 Config 클래스를 사용.

# 데이터베이스 초기화
db.init_app(app)

# UserController의 Blueprint 등록
app.register_blueprint(user_bp)


@app.errorhandler(CustomException)
def custom_exception(e: CustomException):
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
def hello_world():
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
