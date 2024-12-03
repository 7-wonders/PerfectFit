import json
import os

import requests
import torch
from pydantic import ValidationError
# from transformers import AutoTokenizer, AutoModelForCausalLM,pipeline
from openai import OpenAI
from config.config_mysql import get_session
from domain.models import Resume, ResumeSection, WorkExperience, ProjectExperience, Interview, InterviewQuestion, \
    InterviewAnswer, Job

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from dto.interview.interview import InterviewDto
from dotenv import load_dotenv

# load_dotenv()
# OpenAI API 키 가져오기
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def get_dinner_recommendation():
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': '넌 지금부터 유사 백종원 선생이야'},
            {'role': 'user', 'content': '오늘의 저녁 메뉴를 선택 해줘 난 매운게 땡겨'}
        ],
        'max_tokens': 50,
        'temperature': 0.7
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content'].strip()
        print(result)
        return result
    else:
        return f"Error: {response.status_code}, {response.text}"


def make_interview_based_on_resume(resume_id: int, level: str,title: str):

    resume = get_session().query(Resume).filter_by(resume_id=resume_id).first()
    if resume is None:
        raise CustomException(ExceptionType.NOT_FOUND_INTERVIEW) ### resume not found error 추가 요망

    resume_section = get_session().query(ResumeSection).filter_by(resume_id=resume_id).all()
    if resume_section is None:
        raise CustomException(ExceptionType.NOT_FOUND_INTERVIEW) ### resume_section not found error 추가 요망

    work_experience = get_session().query(WorkExperience).filter_by(user_id=resume.user_id).all()
    if work_experience is None:
        raise CustomException(ExceptionType.NOT_FOUND_INTERVIEW) ### work_experience not found error 추가 요망

    project_experience = get_session().query(ProjectExperience).filter_by(user_id=resume.user_id).all()
    if project_experience is None:
        raise CustomException(ExceptionType.NOT_FOUND_INTERVIEW) ### project_experience not found error 추가 요망

    client = OpenAI(api_key=f'{OPENAI_API_KEY}')



    resume_section_content = "\n".join([f"{section.title}: {section.content}" for section in resume_section])

    work_experience_content = "\n".join([
        f"회사명: {exp.company_name} \n"
        f"입사일: {exp.from_date} \n"
        f"퇴사일: {exp.to_date} \n"
        f"퇴사 이유: {exp.reason} \n"
        f"직급/직업: {exp.position} \n"
        f"업무: {exp.responsibility} \n"
        for exp in work_experience
    ])

    project_experience_content = "\n".join([
        f"프로젝트명: {exp.project_name} \n"
        f"프로젝트 시작일: {exp.from_date} \n"
        f"프로젝트 종료일: {exp.to_date} \n"
        f"프로젝트 내용: {{"
        + ", ".join(
            [f"프로젝트 내용{i + 1}: {task.content}" for i, task in enumerate(exp.tasks)]
        ) + "} \n"
        for exp in project_experience
    ])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        temperature=0.7,
        messages=[
            {"role": "system",
             "content": f"You are an interviewer related to {resume.job}. Please ensure to return the response as a JSON object with exactly 10 'Question' and 'BestAnswer' pairs, wrapped under the key 'InterviewQuestions'."},
            {"role": "user", "content": f"당신은 직업 : {resume.job}에 관한 선임자이며 오랜 경력의 전문가입니다. 해당 직무 관련 신입 채용을 위해 면접을 진행해야합니다."},
            {"role": "user",
             "content": "당신은 지금부터 면접을 진행해야 해야합니다. 지원자의 자기소개서 내용을 기반으로 수행을 하되, 내용 기반으로 파생적인 내용을 질문을 해도 괜찮습니다."},
            {"role": "user",
             "content": "자기소개서 내용이 여러개 일 경우, 질문 개수를 가능한 균등하게 분할해주세요."},
            {"role": "user", "content": "이 아래부터는 자기소개서 내용들입니다. 이를 기반으로 한국어로 면접을 진행해주세요."},
            {"role": "user", "content": resume_section_content},
            {"role": "user", "content": "========================================="},
            {"role": "user", "content": "이 아래부터는 지원자의 경력 사항입니다. 공란일 수 있습니다."},
            {"role": "user", "content": work_experience_content},
            {"role": "user", "content": "이 아래부터는 지원자의 프로젝트 경험 사항입니다. 공란일 수 있습니다."},
            {"role": "user", "content": project_experience_content}
        ]
    )
    try:
        result = response.choices[0].message.content.strip()
        print(result)

        interview_data_dict = json.loads(result)
        interview_data = InterviewDto.Response.InterviewResponse.model_validate(interview_data_dict)
        interview_questions = interview_data.InterviewQuestions

        new_interview = Interview(user_id=resume.user_id, resume_id=resume_id, job_id=resume.job_id, company=None, title=title, level = level)
        get_session().add(new_interview)
        get_session().flush()

        interview_id = new_interview.interview_id


        for item in interview_questions:
            question_text = item.Question
            answer_text = item.BestAnswer

            # 질문 저장
            new_question = InterviewQuestion(interview_id=interview_id, question=question_text)
            get_session().add(new_question)
            get_session().flush()

            # 답변 저장
            new_answer = InterviewAnswer(question_id=new_question.question_id, answer=answer_text)
            get_session().add(new_answer)

        # 5. 트랜잭션 커밋
        get_session().commit()

        return result
    except (KeyError, ValidationError) as e:
        get_session().rollback()
        print(f"Error: {e}")
        return None

def make_interview_based_on_job(job_id: int, user_id: int, level: str, title: str):
    job = get_session().query(Job).filter_by(job_id=job_id).first()
    client = OpenAI(api_key=f'{OPENAI_API_KEY}')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        temperature=0.7,
        messages=[
            {"role": "system",
             "content": f"You are an interviewer related to {job.job_name}. Please ensure to return the response as a JSON object with exactly 10 'Question' and 'BestAnswer' pairs, wrapped under the key 'InterviewQuestions'."},
            {"role": "user", "content": f"당신은 직업 : {job.job_name}에 관한 선임자이며 오랜 경력의 전문가입니다. 해당 직무 관련 신입 채용을 위해 면접을 진행해야합니다."},
            {"role": "user",
             "content": "당신은 지금부터 면접을 진행해야 해야합니다. 지원 전공 관련 심화 내용을 위주로 질문해주세요. 이 면접은 직무 면접입니다."},
            {"role": "user",
             "content": f"지원자는 {level}자 입니다."},

        ]
    )
    try:
        result = response.choices[0].message.content.strip()
        print(result)

        new_interview = Interview(user_id=user_id, resume_id=None, job_id=job.job_id, company=None, title=title, level = level)
        get_session().add(new_interview)
        get_session().flush()
        interview_id = new_interview.interview_id
        # interview_data = json.loads(result)
        # interview_questions = interview_data.get("InterviewQuestions", [])
        interview_data_dict = json.loads(result)
        interview_data = InterviewDto.Response.InterviewResponse.model_validate(interview_data_dict)
        interview_questions = interview_data.InterviewQuestions
        print(interview_questions)
        for item in interview_questions:
            question_text = item.Question
            answer_text = item.BestAnswer
            print("1b")
            # 질문 저장
            new_question = InterviewQuestion(interview_id=interview_id, question=question_text)
            get_session().add(new_question)
            get_session().flush()

            # 답변 저장
            new_answer = InterviewAnswer(question_id=new_question.question_id, answer=answer_text)
            get_session().add(new_answer)

        # 5. 트랜잭션 커밋
        get_session().commit()
        print("Data successfully inserted into the database!")

        return interview_id
    except KeyError as e:
        get_session().rollback()
        print(f"Error: {e}")
        return None


def answer_improvement(user_answers: list[str], question_ids: list[int],questions: list[str], best_answers: list[str]):
    client = OpenAI(api_key=f'{OPENAI_API_KEY}')
    results = []
    for question, user_answer, best_answer in zip(questions, user_answers, best_answers):

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
                 "content": f"하지만, 지원자는 {user_answer}라는 답변을 당신에게 하였습니다."},
                {"role": "user",
                 "content": f"당신이 판단하기에 지원자의 답변의 부족한 점과 보완할 점을 찾아 개선사항을 도출하고, 지원자의 답변을 개선하여 알려주세요. 개선 사항과 개선된 문장 모두 한국어로 해주세요."},

            ]
        )

        try:
            result = response.choices[0].message.content.strip()
            print(result)
            try:
                # JSON 문자열을 Python 객체로 변환
                result_dict = json.loads(result)
                print("Parsed result as dict:", result_dict)
                results.append(result_dict)
            except json.JSONDecodeError as e:
                # JSON 디코딩 실패 시 에러 로그 출력
                print("JSONDecodeError:", e)
                raise ValueError("The result is not a valid JSON string.")
        except KeyError as e:
            print(f"Error: {e}")
            return None


# # Llama API 키 가져오기 (가정)
# LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')
#
# base = 'beomi/Llama-3-Open-Ko-8B-Instruct-preview'
# finetuned = 'beomi/KoAlpaca-13B-LoRA'
#
#
# def get_test_llama():
#     url = "http://localhost:11434/api/generate"
#     data = {
#         "model": "llama3.1:latest",
#         "prompt": "<|begin_of_text|><|start_header_id|>너는 IT 기업 채용을 위해 초빙 된, 한국인 면접 전문가야<|end_header_id|> "
#                   "너는 한국어로만 말을 해야해.  " # 역할 지정.
#                   "백엔드 개발자 직군 채용 면접을 진행중이야. 질문을 5개 내줘. "
#                   "추가로 너가 생각하는 이상적인 답변도 덧붙여줘. "
#                   "답변의 구성을  [ 질문, 답변 ] 식으로 구성해. "
#     }
#
#     headers = {'Content-Type': 'application/json'}
#
#     response = requests.post(url, json=data, headers=headers)
#
#     # 개별 JSON 객체로 분할
#     json_objects = response.content.decode().strip().split("\n")
#
#     # 각 JSON 객체를 Python 사전으로 변환
#     data = [json.loads(obj) for obj in json_objects]
#     res_text = ''
#     # 변환된 데이터 출력
#     for item in data:
#         res_text += item['response']
#
#     print(res_text)
#
#     if response.status_code == 200:
#         print('Success')
#     else:
#         print("Error:", response.status_code, response.text)
#
# def get_test_llama_transformers():
#     # Hugging Face의 pipeline 사용
#     model_id = "beomi/KoAlpaca-Polyglot-5.8B"
#
#     pipe = pipeline("text-generation", model=model_id)
#
#     # 프롬프트 설정
#     prompt = "<|begin_of_text|><|start_header_id|>너는 IT 기업 채용을 위해 초빙 된, 한국인 면접 전문가야<|end_header_id|> " \
#              "너는 한국어로만 말을 해야해. " \
#              "백엔드 개발자 직군 채용 면접을 진행중이야. 질문을 5개 만들어줘" \
#
#     # Hugging Face pipeline을 사용하여 응답 생성
#     response = pipe(prompt, max_length=512, num_return_sequences=1)
#
#     # 응답 출력
#     res_text = response[0]['generated_text']
#
#     res_text = response[0]['generated_text']
#
# def get_test_transformers_llama() :
#     # model_id = 'llama3:latest'
#
#     model_id = "beomi/KoAlpaca-Polyglot-5.8B"
#
#     tokenizer = AutoTokenizer.from_pretrained(model_id)
#     model = AutoModelForCausalLM.from_pretrained(
#         model_id,
#         torch_dtype=torch.float16,
#         low_cpu_mem_usage=True,
#     ).to(device=f"cuda", non_blocking=True)
#     model.eval()
#
#     pipe = pipeline(
#         'text-generation',
#         model=model,
#         tokenizer=model_id,
#         device=0
#     )
#     messages = [
#         {"role": "system", "content": "너는 매우 전문적인 시니어 백엔드 개발자. 면접관으로서 참여한거야."},
#         {"role": "user", "content": "백엔드 개발자 주니어 채용 면접 현장에 와있어.너는 면접관으로서 기술에 관련된 질문을 5개 해야해. 질문과 답변 모두 한국어로 해."},
#     ]
#
#     input_ids = tokenizer.apply_chat_template(
#         messages,
#         add_generation_prompt=True,
#         return_tensors="pt"
#     ).to(model.device)
#
#     terminators = [
#         tokenizer.eos_token_id,
#         tokenizer.convert_tokens_to_ids("<|eot_id|>")
#     ]
#
#     outputs = model.generate(
#         input_ids,
#         max_new_tokens=512,
#         eos_token_id=terminators,
#         do_sample=True,
#         temperature=1,
#         top_p=0.9,
#     )
#     response = outputs[0][input_ids.shape[-1]:]
#     print(tokenizer.decode(response, skip_special_tokens=True))