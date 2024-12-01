import os

from celery import Celery
from dotenv import load_dotenv

from domain.models import AppUser, Job, InterviewImprovement
from dto.job.job import JobDto
from dto.resume.resume import ResumeDto
from dto.resume.resume_gpt import ResumeGPT
from utils.celery_util import update_task_status
from utils.open_ai import answer_improvement
from utils.openai.resume.full_resume_strategy import FullResumeStrategy
from utils.openai.resume.resume_helper import ResumeHelper
from config.config_mysql import Config, get_session

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
def add_resume_task(job: Job, user: AppUser, resume: ResumeDto.Request.CreateFullResume):
    resume_helper = ResumeHelper(strategy=FullResumeStrategy(resume=ResumeGPT.Request.FullResume.Create(
        keywords=resume.keywords,
        job_name=job.job_name,
        level=resume.level,
        pros=resume.pros,
        cons=resume.cons,
        directional=resume.directional,
        chapter=resume.chapter,
        work_experiences=user.work_experiences,
        project_experiences=user.project_experiences
    )))

    answer: ResumeGPT.Response.Answer = resume_helper.get_answer()

    return ResumeGPT.Response.FullResume.Resume(
        job_id=job.job_id,
        chapter=resume.chapter,
        keywords=resume.keywords,
        directional=resume.directional,
        cons=resume.cons,
        pros=resume.pros,
        level=resume.level,
        sections=answer.sections,
    )

#
# @app.task
# def start_async_ai_task(user_answer: str, question_id: int, task_id: str):
#     session = get_session()
#     try:
#         improvements = answer_improvement(user_answer, question_id)
#         for improvement in improvements['InterviewImprovement']:
#             new_improvement = InterviewImprovement(
#                 question_id=int(question_id),
#                 answer=improvement['UserAnswer'],
#                 improvement=improvement['Improvement'],
#                 translated_answer=improvement['TranslatedAnswer']
#             )
#             session.add(new_improvement)
#         # 상태 업데이트 (COMPLETED)
#         update_task_status(task_id, status='COMPLETED')
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         update_task_status(task_id, status='FAILED')
#         raise e
