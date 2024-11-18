import os
import time

from celery import Celery
from dotenv import load_dotenv

from domain.models import AppUser
from dto.resume.resume import ResumeDto
from dto.resume.resume_gpt import ResumeGPT
from utils.openai.resume.full_resume_strategy import FullResumeStrategy
from utils.openai.resume.resume_helper import ResumeHelper

load_dotenv()

hostname = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
username = os.getenv("REDIS_USERNAME")
password = os.getenv("REDIS_PASSWORD")
REDIS_URL = f"redis://{username}:{password}@{hostname}:{port}/0"

app = Celery("tasks")

app.conf.update(
    broker_url=REDIS_URL,
    result_backend=REDIS_URL,
    event_serializer='pickle',
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=['application/json', 'application/x-python-serialize'],
    timezone="Asia/Seoul",
    enable_utc=True,
)


@app.task
def add_resume_task(job_name: str, user: AppUser, resume: ResumeDto.Request.CreateFullResume):
    resume_helper = ResumeHelper(strategy=FullResumeStrategy(resume=ResumeGPT.Request.CreateResume(
        keywords=resume.keywords,
        job_name=job_name,
        level=resume.level,
        pros=resume.pros,
        cons=resume.cons,
        directional=resume.directional,
        chapter=resume.chapter,
        work_experiences=user.work_experiences,
        project_experiences=user.project_experiences
    )))

    return resume_helper.get_answer()
