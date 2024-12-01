import json
from dataclasses import asdict

from flask import Blueprint, request, jsonify, Response, render_template, redirect

from dto.interview.interview import InterviewDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from middlewares.auth_middleware import jwt_factory
from services.job_service import JobService
from services.resume_service import ResumeService

from services.interview_service import InterviewService
from utils.celery_util import check_task_status
from utils.jwt_factory import JWTFactory

from utils.open_ai import make_interview_based_on_resume, make_interview_based_on_job
interview_bp = Blueprint('interview', __name__)


@interview_bp.route('/<interview_id>', methods=['GET'])
def get_questions(interview_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    questions: InterviewDto.Response.questions = InterviewService.get_questions(interview_id)

    # response = {
    #     "questions": [{
    #         "questionId": question.question_id,
    #         "question": question.question}
    #         for question in questions.questions],
    #     "total": questions.total
    # }


    response: InterviewDto.Response.QuestionList = InterviewDto.Response.QuestionList(
        questions= [question for question in questions.questions],
        total=questions.total
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')



    # return render_template("test/test_interview.html", response=response)

@interview_bp.route('/ispublic/<interview_id>', methods=['GET']) # Modal 창에 띄울 것이라 Json으로 리턴
def get_is_public(interview_id: int):
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    interviewList = InterviewService.get_is_public(interview_id)

    response: InterviewDto.Response.isPublicList = InterviewDto.Response.isPublicList(
        interviews= [interview for interview in interviewList]
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@interview_bp.route('/improvement/<interview_id>', methods=['GET'])
def get_improvement(interview_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    improvementList = InterviewService.get_improvement(interview_id, user_id)

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

    return render_template("result.html",response=response)


@interview_bp.route('/<interview_id>/like', methods=['POST'])
def post_like(interview_id: int):
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))


    data = request.get_json()
    is_like = data.get("is_like")

    InterviewService.post_like(interview_id,user_id)

    return Response("", status=204)
@interview_bp.route('/<interview_id>/like', methods=['DELETE'])
def delete_like(interview_id: int):
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))


    data = request.get_json()
    is_like = data.get("is_like")
    
    InterviewService.delete_like(interview_id,user_id)
    return Response("", status=204)

@interview_bp.route('/', methods=['POST'])
def post_question_answer():
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    question_id = request.form.get('questionId', None, type=int)
    answer = request.form.get('answer', None, type=str)
    print("Asd")
    # 이전 요청 상태 확인
    existing_task = check_task_status(user_id, question_id)
    print(existing_task)
    if existing_task and existing_task["status"] == 'PENDING':
        return jsonify({"error": "Previous task is still in progress."}), 409

    # 새 작업 추가
    post_answer_request = InterviewDto.Request.postInterviewAnswer(
        questionId=question_id,
        answer=answer
    )

    task = InterviewService.post_question_answer(post_answer_request, user_id)

    print(task)

    return jsonify({"message": "Answer submitted successfully.", "task_id": task.id})



@interview_bp.route('/resume/select', methods=['POST'])
def make_interview_resume():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    # POST 요청에서 form 데이터를 읽어옴
    resume_id = request.form.get('resumeId', None, type=int)
    level = request.form.get('level', None, type=str)
    title = request.form.get('title', None, type=str)

    request_dto = InterviewDto.Request.postMakeInterviewResume(
        resumeId=resume_id,
        level=level,
        title=title
    )

    InterviewService.make_interview_resume(request_dto)

    # 아마 리턴으로 로딩창 혹은 결과페이지로 보내야 할듯.

@interview_bp.route('/job/select', methods=['POST'])
def make_interview_job():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    job_id = request.form.get('jobId', None, type=int)
    level = request.form.get('level', None, type=str)
    title = request.form.get('title', None, type=str)

    request_dto = InterviewDto.Request.postMakeInterviewJob(
        jobId=job_id,
        userId=user_id,
        level=level,
        title=title
    )

    InterviewService.make_interview_job(request_dto)

    return render_template("Loading-create.html") # 임시로 로딩창으로 넘어가게 수정.
    # 추가로 작업 비동기 걸고 통신을 통해 넘어가야함.

@interview_bp.route('/ispublic', methods=['PATCH'])
def patch_is_public():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴. Patch 방식은 Form 사용이 불가능하여 Axios 방식으로 해야할 것으로 예상. 그래서 body를 받음

    is_share_ids = data.get('isShareIds', [])
    is_close_ids = data.get('isCloseIds', [])


    if isinstance(is_share_ids, list):
        InterviewService.patch_ispublic(is_share_ids)
    if isinstance(is_close_ids, list):
        InterviewService.patch_ispublic_cancel(is_close_ids)

    return Response('', status=204, content_type='application/json; charset=utf-8') # 완료 후 어디로 보내야 하나
@interview_bp.route('/ispublic/cancel', methods=['PATCH']) # deprecated
def patch_is_public_cancel():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴
    questionIds: list[int] = request.form.get('questionIds')

    InterviewService.patch_ispublic_cancel(questionIds)


    return Response(' ', status=204, content_type='application/json; charset=utf-8') #

@interview_bp.route('/<interview_id>/title', methods=['PATCH'])
def patch_title(interview_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴. 마찬가지로 Patch 방식이라 Form 불가능
    patch_interview_title = InterviewDto.Request.patchInterviewTitle(**data, interviewId=interview_id)

    InterviewService.patch_interview_title(patch_interview_title)

    return Response(' ', status=204, content_type='application/json; charset=utf-8')

@interview_bp.route('/spellcheck', methods=['GET','POST']) # 프론트가 나와야 테스트 가능
def spell_check():
    if request.method == 'POST':
        # POST 요청에서 폼 데이터를 가져옵니다.
        content = request.form.get('content', None, type=str)
        if content is None :
            content = request.get_json().get('content', None)
        print(content)
        if not content:
            return render_template(
                'spelling_check.html',
                content="",
                translatedContent="문장을 입력해주세요."
            )

        spellCheckDto = InterviewDto.Request.spellCheck(content=content)
        translatedContent = InterviewService.spell_check(spellCheckDto)

        response = {
            "translatedContent": translatedContent
        }
        # 데이터를 HTML에 전달하며 렌더링
        # return render_template(
        #     'spelling_check.html',
        #     content=content,
        #     translatedContent=translatedContent
        # )
        print(jsonify(translatedContent))
        return jsonify(translatedContent), 200
    # GET 요청 처리 (기본 빈 페이지 렌더링)
    return render_template(
        'spelling_check.html',
        content="",
        translatedContent=""
    )


@interview_bp.route('/loading-create')
def loading_create():
    return render_template("Loading-create.html")

@interview_bp.route('/loading-analyze')
def loading_analyze():
    return render_template("Loading-analyze.html")

@interview_bp.route('/')
def interview():
    return render_template("interview.html")

@interview_bp.route('/list') # 모의면접 목록 페이지.
def interviewlist():
    """
    기업별 리스트 가져올 모의면접.

1. is_public : true
2. company : not null
3. 사용자 이름 넣고 제목 설정
    1. 윤**님 AI 모의면접
4. 회사가 있으니까 인재상 있으므로 넣어줌
5. 학교이름은 그냥 명시해서 넣기.
6. 경력도 그냥 넣기

지원분야별

1. is_public : true
2. occupation_id 별로 넣기
3. 일단 인재상 . 다빼기
4. 최상단 회사명은 있는 경우에만 넣기
    1. 없으면 그냥 비어두기
5. 기타 사항은 기업별과 동일
    :return:
    """
    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    job_interviews, company_interviews = InterviewService.get_interview_list()

    keyword = request.form.get('keyword', None, type=str)
    if keyword is None :
        response = {
            "companyInterviews" : [{
                    "interviewId" : company_interview.interviewId,
                    "companyName" : company_interview.companyName,
                    "level" : company_interview.level,
                    "title" : company_interview.title,
                    "jobName" : company_interview.jobName, # 지원 분야
                    "university": company_interview.university, # 출신 학교
                    "companyBest": [company_best.content for company_best in company_interview.companyBest],
                    "companyWorst": company_interview.companyWorst
                } for company_interview in company_interviews],
            "jobInterviews": [{
                "occupationId": job_interview['occupationId'],
                "interviews": [{
                    "interviewId": interview.interviewId,
                    "companyName": ( interview.companyName if interview.companyName else None ),
                    "level": interview.level,
                    "title": interview.title,
                    "jobName": interview.jobName,  # 지원 분야
                    "university": interview.university  # 출신 학교
                 } for interview in job_interview['jobInterviews']],
                "total": job_interview['total']
            } for job_interview in job_interviews],
            "searchInterviews": [],
            "total" : len(job_interviews) # job_interviews는 무조건 들어가니까 이거로
        }
    else :
        search_interviews = InterviewService.get_interview_list_search(keyword)
        response = {
            "companyInterviews": [{
                "interviewId": company_interview.interviewId,
                "questionId": company_interview.questionId,
                "companyName": company_interview.companyName,
                "level": company_interview.level,
                "title": company_interview.title,
                "jobName": company_interview.jobName,  # 지원 분야
                "university": company_interview.university,  # 출신 학교
                "companyBest": [company_best.content for company_best in company_interview.companyBest],
                "companyWorst": company_interview.companyWorst
            } for company_interview in company_interviews],
            "jobInterviews": [{
                "occupationId": job_interview['occupationId'],
                "interviews": [{
                    "interviewId": interview.interviewId,
                    "questionId": interview.questionId,
                    "companyName": (interview.companyName if interview.companyName else None),
                    "level": interview.level,
                    "title": interview.title,
                    "jobName": interview.jobName,  # 지원 분야
                    "university": interview.university  # 출신 학교
                } for interview in job_interview['jobInterviews']],
                "total": job_interview['total']
            } for job_interview in job_interviews],
            "searchInterviews": [{
                "interviewId": search_interview.interviewId,
                "questionId": search_interview.questionId,
                "companyName": search_interview.companyName,
                "level": search_interview.level,
                "title": search_interview.title,
                "jobName": search_interview.jobName,  # 지원 분야
                "university": search_interview.university,  # 출신 학교
                "companyBest": [company_best.content for company_best in search_interview.companyBest] if search_interview.companyName else None,
                "companyWorst": search_interview.companyWorst if search_interview.companyName else None
            } for search_interview in search_interviews],
            "total": len(job_interviews)
        }

    return render_template("interviewlist.html", response = response)

@interview_bp.route('/result') # 모의면접 결과 페이지. Improvement
def result():
    return render_template("result.html")

@interview_bp.route('/resume-select') # api 추가하였음.
def resume_select():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))


    resume_list, total = ResumeService.get_my_resumes(user_id,1,100) # 일단 100개 가져오기

    response = {
        "resumes": [{
            "resumeId": resume.resume_id,
            "title": resume.title,
            "level": resume.level,
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

@interview_bp.route('/run/<interview_id>')
def interview_run(interview_id: int):
    return render_template("interview.html", interviewId = interview_id)

