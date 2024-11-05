import json
from dataclasses import asdict

from flask import Blueprint, request, jsonify, Response

from dto.interview.interview import InterviewDto

from services.interview_service import InterviewService
from hanspell import spell_checker
import re, requests

interview_bp = Blueprint('interview', __name__)


@interview_bp.route('/interview/<resume_id>', methods=['GET'])
def get_questions(resume_id: int):

    questions = InterviewService.get_questions(resume_id)
    response: InterviewDto.Response.questions = InterviewDto.Response.questions(
        questions=
        [InterviewDto.Response.interviewQuestion(question.question_id, question.question)
            for question in questions],
        total=len(questions)
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@interview_bp.route('/interview/ispublic/<interview_id>', methods=['GET'])
def get_is_public(interview_id: int):

    interviewList = InterviewService.get_is_public(interview_id)
    response: InterviewDto.Response.isPublicList = InterviewDto.Response.isPublicList(
        interviews= [interview for interview in interviewList]
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')


@interview_bp.route('/interview', methods=['POST'])
def post_question_answer():

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    post_answer_request = InterviewDto.Request.postInterviewAnswer(**data)

    InterviewService.post_question_answer(post_answer_request)


    return Response(' ', status=201, content_type='application/json; charset=utf-8')

@interview_bp.route('/spell', methods=['GET'])
def spell_tester() -> None:
    text = "안녕 하세요. 만나서 반갑 습니다."
    print('WORKING#############################')
    try:
        passportKey = get_passport_key()

        # 맞춤법 검사 수행
        result = spell_checker.check(text,passportKey)

        # 결과 출력
        print("Checked Text:", result.checked)  # 수정된 텍스트
        print("Original Text:", result.original)  # 원본 텍스트
        print("Errors Found:", result.errors)  # 발견된 오류 수
        print("Corrections:", result.words)  # 각 단어의 교정 결과

    except Exception as e:
        print("Error occurred:", e)

def get_passport_key():
    """네이버에서 '네이버 맞춤법 검사기' 페이지에서 passportKey를 획득

        - 네이버에서 '네이버 맞춤법 검사기'를 띄운 후
        html에서 passportKey를 검색하면 값을 찾을 수 있다.

        - 찾은 값을 spell_checker.py 48 line에 적용한다.
    """

    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=네이버+맞춤법+검사기"
    res = requests.get(url)

    html_text = res.text

    match = re.search(r'passportKey=([^&"}]+)', html_text)
    if match:
        passport_key = match.group(1)
        return passport_key
    else:
        return False
