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


@interview_bp.route('/interview', methods=['POST','GET'])
def post_question_answer():

    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    ##data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    ##post_answer_request = InterviewDto.Request.postInterviewAnswer(**data)

    post_answer_request = InterviewDto.Request.postInterviewAnswer(questionId=14,answer="이커머스 플랫폼이 활약하는 이 의류라는 분야는 단순히 보면 작아보일 수 있는 산업이지만, 의식주라는 말이 있듯이 사람이 삶을 영위하는데에 있어서 필수적인 요소입니다. 그렇기에 저는 앞으로도 마르지 않는 샘물처럼 산업이 성장해나갈 플랫폼에 매료되었다고 말씀드리고 싶습니다. 그 중에서 저는 특히 AI는 매력적이라고 생각하는데요. 왜냐하면 이를 잘 활용하여 접근성을 높인다면, IT에 약하기에 아직 소외되고 있는 잠재적 고객층인 실버층을 타겟으로 공격적인 마케팅이 가능하다고 생각했기 때문입니다. 예를들어 정말 불필요한 UI요소를 다 빼고, 어르신이 말하는 직관적인 자연어를 해석해서 필요한 옷을 추천해줄 수 있다면 이는 정말 매력적이라고 생각합니다.")


    InterviewService.post_question_answer(post_answer_request)

    # 여기서 개선사항 도출해야함.

    return Response(' ', status=201, content_type='application/json; charset=utf-8')

@interview_bp.route('/interview/ispublic', methods=['PATCH'])
def patch_is_public():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
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