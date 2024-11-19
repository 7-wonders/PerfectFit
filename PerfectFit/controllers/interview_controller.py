import json
from dataclasses import asdict

from flask import Blueprint, request, jsonify, Response

from dto.interview.interview import InterviewDto

from services.interview_service import InterviewService
from utils.jwt_factory import JWTFactory

from utils.open_ai import make_interview_based_on_resume, make_interview_based_on_job
interview_bp = Blueprint('interview', __name__)


@interview_bp.route('/interview/<resume_id>', methods=['GET'])
def get_questions(resume_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

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

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    interviewList = InterviewService.get_is_public(interview_id)
    response: InterviewDto.Response.isPublicList = InterviewDto.Response.isPublicList(
        interviews= [interview for interview in interviewList]
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@interview_bp.route('/interview/improvement/<interview_id>', methods=['GET'])
def get_improvement(interview_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    improvementList = InterviewService.get_improvement(interview_id)
    response: InterviewDto.Response.improvementList = InterviewDto.Response.improvementList(
        improvements= [improvement for improvement in improvementList]
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')


@interview_bp.route('/interview', methods=['POST'])
def post_question_answer():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    post_answer_request = InterviewDto.Request.postInterviewAnswer(**data)

    InterviewService.post_question_answer(post_answer_request)

    # 여기서 개선사항 도출해야함.

    return Response(' ', status=201, content_type='application/json; charset=utf-8')

@interview_bp.route('/interview/ispublic', methods=['PATCH'])
def patch_is_public():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    print(data)
    questionIds: list[int] = data.get('questionIds')

    InterviewService.patch_ispublic(questionIds)


    return Response(' ', status=204, content_type='application/json; charset=utf-8')
@interview_bp.route('/interview/ispublic/cancel', methods=['PATCH'])
def patch_is_public_cancel():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    print(data)
    questionIds: list[int] = data.get('questionIds')

    InterviewService.patch_ispublic_cancel(questionIds)


    return Response(' ', status=204, content_type='application/json; charset=utf-8')
@interview_bp.route('/interview/<interview_id>/title', methods=['PATCH'])
def patch_title(interview_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    patch_interview_title = InterviewDto.Request.patchInterviewTitle(**data, interviewId=interview_id)

    InterviewService.patch_interview_title(patch_interview_title)

    return Response(' ', status=204, content_type='application/json; charset=utf-8')


@interview_bp.route('/spellcheck', methods=['POST'])
def spell_check():

    data = request.get_json()  # POST 요청의 BODY 가져오기.
    spellCheckDto = InterviewDto.Request.spellCheck(**data)

    translatedContent = InterviewService.spell_check(spellCheckDto)

    response: InterviewDto.Response.spellChecked = InterviewDto.Response.spellChecked(
        translatedContent= translatedContent
    )
    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@interview_bp.route('/testGPT',methods=['GET'])
def gpt():
    make_interview_based_on_resume(1,"신입")

@interview_bp.route('/testGPT2', methods=['GET'])
def gpt2():
    make_interview_based_on_job(254, 1,"경력")