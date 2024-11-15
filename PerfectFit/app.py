import os

from flask import Flask, render_template

from controllers.interview_controller import interview_bp
from database.config import Config, db  # Config와 db를 import
from controllers.user_controller import user_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)  # config.py의 Config 클래스를 사용

# 데이터베이스 초기화
db.init_app(app)

# UserController의 Blueprint 등록
app.register_blueprint(user_bp)
app.register_blueprint(interview_bp, url_prefix="/interview")


@app.route('/')
def loading_create():
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
