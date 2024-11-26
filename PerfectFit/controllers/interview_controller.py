import json
from dataclasses import asdict

from flask import Blueprint, request, jsonify, Response, render_template, redirect

from dto.interview.interview import InterviewDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from services.job_service import JobService
from services.resume_service import ResumeService

from services.interview_service import InterviewService
from utils.jwt_factory import JWTFactory

from utils.open_ai import make_interview_based_on_resume, make_interview_based_on_job
interview_bp = Blueprint('interview', __name__)


@interview_bp.route('/<interview_id>', methods=['GET'])
def get_questions(interview_id: int):

    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    questions: InterviewDto.Response.questions = InterviewService.get_questions(interview_id)
    # json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)
    # return Response(json_response, status=200, content_type='application/json; charset=utf-8')

    print("#############")
    print(questions)

    response = {
        "questions": [{
            "questionId": question.question_id,
            "question": question.question}
            for question in questions.questions],
        "total": questions.total
    }

    return render_template("test/test_interview.html", response=response)

@interview_bp.route('/ispublic/<interview_id>', methods=['GET'])
def get_is_public(interview_id: int):
    print(request.cookies.get('access_token'))
    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    interviewList = InterviewService.get_is_public(interview_id)
    response: InterviewDto.Response.isPublicList = InterviewDto.Response.isPublicList(
        interviews= [interview for interview in interviewList]
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@interview_bp.route('/improvement/<interview_id>', methods=['GET'])
def get_improvement(interview_id: int):

    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    improvementList = InterviewService.get_improvement(interview_id)
    # response: InterviewDto.Response.improvementList = InterviewDto.Response.improvementList(
    #     improvements= [improvement for improvement in improvementList]
    # )
    #
    # json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    response = {
        "improvements": [{
			"improvementId": improvement.improvementId,
			"questionId": improvement.questionId,
			"answer": improvement.answer,
			"improvement": improvement.improvement,
			"translatedAnswer": improvement.translatedAnswer,
		}
            for improvement in improvementList]
    }


    return render_template("test/test.html",response=response)


@interview_bp.route('/interview', methods=['POST'])
def post_question_answer():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    ##data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    ##post_answer_request = InterviewDto.Request.postInterviewAnswer(**data)

    # POST 요청에서 form 데이터를 읽어옴
    question_id = request.form.get('questionId', None, type=int)
    answer = request.form.get('answer', None, type=str)
    print(answer)

    # 디버깅: 데이터 출력
    # DTO 생성
    post_answer_request = InterviewDto.Request.postInterviewAnswer(
        questionId=question_id,
        answer=answer
    )
    InterviewService.post_question_answer(post_answer_request)



    return redirect('/test/test_interview_post.html')

@interview_bp.route('/resume/select', methods=['POST'])
def make_interview_resume():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    # POST 요청에서 form 데이터를 읽어옴
    resume_id = request.form.get('resumeId', None, type=int)
    level = request.form.get('level', None, type=str)
    title = request.form.get('title', None, type=str)

    # 디버깅: 데이터 출력
    # DTO 생성
    request_dto = InterviewDto.Request.postMakeInterviewResume(
        resumeId=resume_id,
        level=level,
        title=title
    )

    InterviewService.make_interview_resume(request_dto)

@interview_bp.route('/job/select', methods=['POST'])
def make_interview_job():
    print("들어옴")
    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))
    user_id = 1
    # POST 요청에서 form 데이터를 읽어옴
    job_id = request.form.get('jobId', None, type=int)
    level = request.form.get('level', None, type=str)
    title = request.form.get('title', None, type=str)

    # 디버깅: 데이터 출력
    # DTO 생성
    request_dto = InterviewDto.Request.postMakeInterviewJob(
        jobId=job_id,
        userId=user_id,
        level=level,
        title=title
    )

    InterviewService.make_interview_job(request_dto)

    return render_template("Loading-create.html")



@interview_bp.route('/ispublic', methods=['PATCH'])
def patch_is_public():

    # jwt_factory = JWTFactory()
    # user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴

    is_share_ids = data.get('isShareIds', [])
    is_close_ids = data.get('isCloseIds', [])


    if isinstance(is_share_ids, list):
        InterviewService.patch_ispublic(is_share_ids)
    if isinstance(is_close_ids, list):
        InterviewService.patch_ispublic_cancel(is_close_ids)

    return Response(' ', status=204, content_type='application/json; charset=utf-8')
@interview_bp.route('/ispublic/cancel', methods=['PATCH'])
def patch_is_public_cancel():

    # jwt_factory = JWTFactory()
    # user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    print(data)
    questionIds: list[int] = request.form.get('questionIds')

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
    if request.method == 'POST':
        # POST 요청에서 폼 데이터를 가져옵니다.
        content = request.form.get('content', None, type=str)
        if not content:
            return render_template(
                'test/test_spellchecker.html',
                content="",
                translatedContent="문장을 입력해주세요."
            )

        spellCheckDto = InterviewDto.Request.spellCheck(content=content)
        translatedContent = InterviewService.spell_check(spellCheckDto)
        # 데이터를 HTML에 전달하며 렌더링
        return render_template(
            'test/test_spellchecker.html',
            content=content,
            translatedContent=translatedContent
        )
    # GET 요청 처리 (기본 빈 페이지 렌더링)
    return render_template(
        'test/test_spellchecker.html',
        content="",
        translatedContent=""
    )
    # data = request.get_json()  # POST 요청의 BODY 가져오기.
    #
    # print("debug1")
    # response: InterviewDto.Response.spellChecked = InterviewDto.Response.spellChecked(
    #     translatedContent= translatedContent
    # )
    # json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)
    # print(response.translatedContent)
    # # return Response(json_response, status=200, content_type='application/json; charset=utf-8')
    # return jsonify(asdict(response)), 200

@interview_bp.route('/testGPT',methods=['GET'])
def gpt():
    make_interview_based_on_resume(1,"신입")

@interview_bp.route('/testGPT2', methods=['GET'])
def gpt2():
    make_interview_based_on_job(254, 1,"경력")

@interview_bp.route('/test/interview/post', methods=['GET'])
def post_test():
    return render_template('test/test_interview_post.html')
  
@interview_bp.route('/test/spellcheck', methods=['GET'])
def spellcheck_test():
    return render_template('test/test_spellchecker.html')

@interview_bp.route('/test/ispublic', methods=['GET'])
def ispublic_test():
    return render_template('test/test_ispublic.html')

@interview_bp.route('/loading')
def loading_create():
    return render_template("Loading-create.html")

@interview_bp.route('/loading-analyze')
def loading_analyze():
    return render_template("Loading-analyze.html")

@interview_bp.route('/')
def interview():
    return render_template("interview.html")

@interview_bp.route('/list')
def interviewlist():
    return render_template("interviewlist.html")

@interview_bp.route('/result')
def result():
    return render_template("result.html")

@interview_bp.route('/resume-select')
def resume_select():

    # jwt_factory = JWTFactory()
    # user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))
    user_id=1

    resume_list, total = ResumeService.get_my_resumes(user_id,1,100) # 일단 100개 가져오기

    response = {
        "resumes": [{
            "resumeId": resume.resume_id,
            "title": resume.title,
            "jobName": resume.job.job_name,
            "createdTime": resume.created_time.strftime("%Y-%m-%d %H:%M")}
            for resume in resume_list],  # JSON 형태로 변환
        "total": total
    }
    print(response)

    return render_template("interview_resume_select.html", response = response)

@interview_bp.route('/job-select')
def job_select():
    job_list = JobService.get_all()
    return render_template("interview_job_select.html", response = job_list)
