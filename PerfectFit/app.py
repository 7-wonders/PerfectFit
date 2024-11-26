
from flask import Flask, render_template, send_from_directory

from controllers.job_controller import job_bp
from controllers.interview_controller import interview_bp

from dotenv import load_dotenv

from config.config_mysql import Config, db  # Config와 db를 import
from config.config_redis import Redis
from controllers.resume_controller import resume_bp
from controllers.resume_draft_controller import resume_draft_bp
from controllers.user_controller import user_bp
from controllers.auth_controller import auth_bp
from exception.exception_handler import eh_bp
from middlewares.auth_middleware import authenticate_request
from utils.jwt_factory import JWTFactory

load_dotenv()

app = Flask(__name__, template_folder="templates")

app.config.from_object(Config)  # config.py의 Config 클래스를 사용

app.register_blueprint(eh_bp)
app.register_blueprint(user_bp)
app.register_blueprint(job_bp)
app.register_blueprint(interview_bp, url_prefix='/interview')
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(resume_bp, url_prefix="/resume")
app.register_blueprint(resume_draft_bp, url_prefix="/resume/draft")

app.before_request(authenticate_request)

# 데이터베이스 초기화
db.init_app(app)

# Redis 초기화
Redis().initialize_pool()
JWTFactory().initialize_pool()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template("main.html")


if __name__ == '__main__':
    app.run()