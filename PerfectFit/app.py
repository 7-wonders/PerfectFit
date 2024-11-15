import os

from flask import Flask, render_template
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


@app.route('/')
def loading_create():
    return render_template("Loading-create.html")
@app.route('/loading-analyze')
def loading_analyze():
    return render_template("Loading-analyze.html")
@app.route('/interview')
def interview():
    return render_template("interview.html")
@app.route('/interviewlist')
def interviewlist():
    return render_template("interviewlist.html")
@app.route('/result')
def result():
    return render_template("result.html")
if __name__ == '__main__':
    app.run()
