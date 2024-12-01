import os
import json

from celery import Celery
from dotenv import load_dotenv
from openai import OpenAI

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
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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
def start_async_ai_task(user_answers: list[str], question_ids: list[int],questions: list[str], best_answers: list[str]):
    print("나는 들어왔다.")
    try:
        client = OpenAI(api_key=f'{OPENAI_API_KEY}')
        results = []
        for question,question_id,user_answer, best_answer in zip(questions,question_ids, user_answers, best_answers):
            print(question, user_answer, best_answer, " :: 수행 시작 ")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                temperature=0.7,
                messages=[
                    {"role": "system",
                     "content": f"You are an interviewer. Please ensure to return the response as a JSON object with exactly 10 'UserAnswer' and 'Improvement' and 'TranslatedAnswer', wrapped under the key 'InterviewImprovement'."
                                f"'UserAnswer' muse be included from '{user_answer}'"
                                f"you must 'TranslatedAnswer' and 'Improvement' used Korean"},
                    {"role": "user",
                     "content": f"당신은 면접관으로서 {question}라는 질문을 하였었습니다."},
                    {"role": "user",
                     "content": f"당신은 {best_answer}라는 답변이 가장 이상적인 답변이라고 생각합니다.."},
                    {"role": "user",
                     "content": f"하지만, 지원자는 {question_id}번 질문에 대해 {user_answer}라는 답변을 당신에게 하였습니다."},
                    {"role": "user",
                     "content": f"당신이 판단하기에 지원자의 답변의 부족한 점과 보완할 점을 찾아 개선사항을 도출하고, 지원자의 답변을 개선하여 알려주세요. 개선 사항과 개선된 문장 모두 한국어로 해주세요."},
                    {"role": "user",
                     "content": f"결과적으로 당신이 나에게 주어야할 답변은 json 형식이고, 다음의 내용이 포함되어야합니다.\n 1. questionId : {question_id} \n 2, question : {question}, \n3, UserAnswer : {user_answer}, \n4. Improvement : 당신이 생각하는 개선점 ,\n5. TranslatedAnswer : 당신이 생각한 개선점으로 UserAnswer를 고친 한국어 문장 "},
                ]
            )

            try:
                result = response.choices[0].message.content.strip()
                try:
                    # JSON 문자열을 Python 객체로 변환
                    result_dict = json.loads(result)
                    result_dict['InterviewImprovement']['UserAnswer'] = user_answer
                    results.append(result_dict)
                except json.JSONDecodeError as e:
                    # JSON 디코딩 실패 시 에러 로그 출력
                    print("JSONDecodeError:", e)
                    raise ValueError("The result is not a valid JSON string.")
            except KeyError as e:
                print(f"Error: {e}")
                return None

        return results

    except Exception as e:
        raise e



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
