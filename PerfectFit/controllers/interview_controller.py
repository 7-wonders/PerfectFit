import json
from dataclasses import asdict

from flask import Blueprint, request, jsonify, Response

from domain.models import Occupation
from dto.interview.interview import InterviewDto
from dto.job.job import JobDto

from services.interview_service import InterviewService

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

@interview_bp.route('/interview', methods=['POST'])
def post_question_answer():

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    post_answer_request = InterviewDto.Request.postInterviewAnswer(**data)

    InterviewService.post_question_answer(post_answer_request)


    return Response(' ', status=201, content_type='application/json; charset=utf-8')
