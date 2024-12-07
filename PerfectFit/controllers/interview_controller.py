import json
from dataclasses import asdict
from http import HTTPStatus

from flask import Blueprint, request, jsonify, Response, render_template, redirect

from dto.interview.interview import InterviewDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from services.job_service import JobService
from services.resume_service import ResumeService

from services.interview_service import InterviewService
from utils.jwt_factory import JWTFactory

from tasks import start_async_ai_task
from utils.open_ai import make_company_interview, make_company_improvement
interview_bp = Blueprint('interview', __name__)


@interview_bp.route('/<interview_id>', methods=['GET'])
def get_questions(interview_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    questions: InterviewDto.Response.Questions = InterviewService.get_questions(interview_id)

    response: InterviewDto.Response.QuestionList = InterviewDto.Response.QuestionList(
        questions= [question for question in questions.questions],
        total=questions.total
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')


@interview_bp.route('/ispublic/<interview_id>', methods=['GET']) # Modal 창에 띄울 것이라 Json으로 리턴
def get_is_public(interview_id: int):
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    interviewList = InterviewService.get_is_public(interview_id)

    response: InterviewDto.Response.isPublicList = InterviewDto.Response.IsPublicList(
        interviews= [interview for interview in interviewList]
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)

    return Response(json_response, status=200, content_type='application/json; charset=utf-8')


@interview_bp.route('/improvement/task/<task_id>', methods=['GET'])
def get_improvement(task_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    improvementList, is_mine, is_like, view_count, like_count = InterviewService.get_improvement(task_id, user_id)


    title, interview_id = InterviewService.get_interview_title(improvementList[0].questionId, None)

    response = {
        "improvements": [{
			"improvementId": improvement.improvementId,
			"questionId": improvement.questionId,
            "question": improvement.question,
			"answer": improvement.answer,
            "improvement": improvement.improvement.replace("'", '').replace('"', ""),
            "translatedAnswer": improvement.translatedAnswer.replace("'", '').replace('"', ""),
            "isShared": InterviewService.get_question_is_shared(improvement.questionId)
		} for improvement in improvementList],
        "title" : title,
        "isMine" : is_mine,
        "isLike" : is_like,
        "viewCount" : view_count,
        "likeCount" : like_count,
        "interviewId": interview_id,
    }

    return render_template("interview_improvement.html",response=response)


@interview_bp.route('/improvement/<interview_id>', methods=['GET'])
def get_improvement_with_id(interview_id: int):

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    improvementList, is_mine, is_like, view_count, like_count = InterviewService.get_improvement_based_id(interview_id, user_id)

    title, interview_id = InterviewService.get_interview_title(None, interview_id)
    response = {
        "improvements": [{
			"improvementId": improvement.improvementId,
			"questionId": improvement.questionId,
            "question": improvement.question,
			"answer": improvement.answer,
            "improvement": improvement.improvement.replace("'", '').replace('"', ""),
            "translatedAnswer": improvement.translatedAnswer.replace("'", '').replace('"', ""),
            "isShared": InterviewService.get_question_is_shared(improvement.questionId)
		}
            for improvement in improvementList],
        "title" : title,
        "isMine" : is_mine,
        "isLike" : is_like,
        "viewCount" : view_count,
        "likeCount" : like_count,
        "interviewId" : interview_id
    }

    return render_template("interview_improvement.html",response=response)


@interview_bp.route('/<interview_id>/like', methods=['POST'])
def post_like(interview_id: int):
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    InterviewService.post_like(interview_id,user_id)

    return Response("", status=204)


@interview_bp.route('/<interview_id>/like', methods=['DELETE'])
def delete_like(interview_id: int):
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    InterviewService.delete_like(interview_id,user_id)
    return Response("", status=204)


@interview_bp.route('/<interview_id>', methods=['DELETE'])
def delete_interview(interview_id: int):
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    InterviewService.delete_interview(interview_id, user_id)
    return Response("", status=204)


@interview_bp.route('/', methods=['POST'])
def post_question_answer():
    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))
    print(request.form.get('questionIds'))
    print(request.form.get('answers'))
    question_ids = [int(qid) for qid in request.form.get('questionIds').split('|') if qid]

    answers = request.form.get('answers').split("|")

    post_answer_request = InterviewDto.Request.PostInterviewAnswer(
        questionIds=question_ids,
        answers=answers
    )

    task = InterviewService.post_question_answer(post_answer_request, user_id)
    print("controller ========" , task.id)

    return jsonify(task.id)


@interview_bp.route('/task/<task_id>', methods=['POST'])
def get_task(task_id):
    task = start_async_ai_task.AsyncResult(task_id)
    state = task.state.lower()

    if state == 'success':

        #여기서 DB 작업
        InterviewService.post_question_answer_after(task_id)

        return jsonify({"task_id": task.id}), HTTPStatus.OK
    elif state == 'failure':
        raise CustomException(ExceptionType.CELERY_ERROR)
    else:
        return {}, HTTPStatus.ACCEPTED


@interview_bp.route('/resume/select', methods=['POST'])
def make_interview_resume():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    # POST 요청에서 form 데이터를 읽어옴
    resume_id = request.form.get('resumeId', None, type=int)
    level = request.form.get('level', None, type=str)
    title = request.form.get('title', None, type=str)

    request_dto = InterviewDto.Request.PostMakeInterviewResume(
        resumeId=resume_id,
        level=level,
        title=title
    )

    interview_id = InterviewService.make_interview_resume(request_dto)


    return redirect(f"/interview/run/{interview_id}")
    # 아마 리턴으로 로딩창 혹은 결과페이지로 보내야 할듯.


@interview_bp.route('/job/select', methods=['POST'])
def make_interview_job():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    job_id = request.form.get('jobId', None, type=int)
    level = request.form.get('level', None, type=str)
    title = request.form.get('title', None, type=str)

    request_dto = InterviewDto.Request.PostMakeInterviewJob(
        jobId=job_id,
        userId=user_id,
        level=level,
        title=title
    )

    interview_id = InterviewService.make_interview_job(request_dto)

    return redirect(f"/interview/run/{interview_id}")
    # return render_template("interview.html",interview_id=interview_id)


@interview_bp.route('/ispublic', methods=['PATCH'])
def patch_is_public():

    jwt_factory = JWTFactory()
    user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    data = request.get_json()  # POST 요청의 JSON 데이터를 가져옴. Patch 방식은 Form 사용이 불가능하여 Axios 방식으로 해야할 것으로 예상. 그래서 body를 받음

    is_share_ids = data.get('isShareIds', [])
    is_close_ids = data.get('isCloseIds', [])


    if isinstance(is_share_ids, list):
        InterviewService.patch_ispublic(is_share_ids, user_id)
    if isinstance(is_close_ids, list):
        InterviewService.patch_ispublic_cancel(is_close_ids, user_id)

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
    patch_interview_title = InterviewDto.Request.PatchInterviewTitle(**data, interviewId=interview_id)

    InterviewService.patch_interview_title(patch_interview_title, user_id)

    return Response(' ', status=204, content_type='application/json; charset=utf-8')


@interview_bp.route('/spellcheck', methods=['GET','POST']) # 프론트가 나와야 테스트 가능
def spell_check():
    if request.method == 'POST':
        # POST 요청에서 폼 데이터를 가져옵니다.
        content = request.form.get('content', None, type=str)

        if content is None :
            content = request.get_json().get('content', None)

        if not content:
            return render_template(
                'spelling_check.html',
                content="",
                translatedContent="문장을 입력해주세요."
            )

        spellCheckDto = InterviewDto.Request.SpellCheck(content=content)
        translatedContent = InterviewService.spell_check(spellCheckDto)

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


@interview_bp.route('/loading-analyze/<task_id>')
def loading_analyze(task_id: int):
    return render_template("Loading-analyze.html", task_id=task_id)


@interview_bp.route('/')
def interview():
    return render_template("interview.html")

# @interview_bp.route('/list') # 모의면접 목록 페이지.
# def interviewlist():
#     """
#     기업별 리스트 가져올 모의면접.
#
# 1. is_public : true
# 2. company : not null
# 3. 사용자 이름 넣고 제목 설정
#     1. 윤**님 AI 모의면접
# 4. 회사가 있으니까 인재상 있으므로 넣어줌
# 5. 학교이름은 그냥 명시해서 넣기.
# 6. 경력도 그냥 넣기
#
# 지원분야별
#
# 1. is_public : true
# 2. occupation_id 별로 넣기
# 3. 일단 인재상 . 다빼기
# 4. 최상단 회사명은 있는 경우에만 넣기
#     1. 없으면 그냥 비어두기
# 5. 기타 사항은 기업별과 동일
#     :return:
#     """
#     #jwt_factory = JWTFactory()
#     #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))
#
#     job_interviews, company_interviews = InterviewService.get_interview_list()
#
#     keyword = request.form.get('keyword', None, type=str)
#     if keyword is None :
#         response = {
#             "companyInterviews" : [{
#                     "interviewId" : company_interview.interviewId,
#                     "companyName" : company_interview.companyName,
#                     "level" : company_interview.level,
#                     "title" : company_interview.title,
#                     "jobName" : company_interview.jobName, # 지원 분야
#                     "university": company_interview.university, # 출신 학교
#                     "companyBest": [company_best.content for company_best in company_interview.companyBest],
#                     "companyWorst": company_interview.companyWorst
#                 } for company_interview in company_interviews],
#             "jobInterviews": [{
#                 "occupationId": job_interview['occupationId'],
#                 "interviews": [{
#                     "interviewId": interview.interviewId,
#                     "companyName": ( interview.companyName if interview.companyName else None ),
#                     "level": interview.level,
#                     "title": interview.title,
#                     "jobName": interview.jobName,  # 지원 분야
#                     "university": interview.university  # 출신 학교
#                  } for interview in job_interview['jobInterviews']],
#                 "total": job_interview['total']
#             } for job_interview in job_interviews],
#             "searchInterviews": [],
#             "total" : len(job_interviews) # job_interviews는 무조건 들어가니까 이거로
#         }
#     else :
#         search_interviews = InterviewService.get_interview_list_search(keyword)
#         response = {
#             "companyInterviews": [{
#                 "interviewId": company_interview.interviewId,
#                 "questionId": company_interview.questionId,
#                 "companyName": company_interview.companyName,
#                 "level": company_interview.level,
#                 "title": company_interview.title,
#                 "jobName": company_interview.jobName,  # 지원 분야
#                 "university": company_interview.university,  # 출신 학교
#                 "companyBest": [company_best.content for company_best in company_interview.companyBest],
#                 "companyWorst": company_interview.companyWorst
#             } for company_interview in company_interviews],
#             "jobInterviews": [{
#                 "occupationId": job_interview['occupationId'],
#                 "interviews": [{
#                     "interviewId": interview.interviewId,
#                     "questionId": interview.questionId,
#                     "companyName": (interview.companyName if interview.companyName else None),
#                     "level": interview.level,
#                     "title": interview.title,
#                     "jobName": interview.jobName,  # 지원 분야
#                     "university": interview.university  # 출신 학교
#                 } for interview in job_interview['jobInterviews']],
#                 "total": job_interview['total']
#             } for job_interview in job_interviews],
#             "searchInterviews": [{
#                 "interviewId": search_interview.interviewId,
#                 "questionId": search_interview.questionId,
#                 "companyName": search_interview.companyName,
#                 "level": search_interview.level,
#                 "title": search_interview.title,
#                 "jobName": search_interview.jobName,  # 지원 분야
#                 "university": search_interview.university,  # 출신 학교
#                 "companyBest": [company_best.content for company_best in search_interview.companyBest] if search_interview.companyName else None,
#                 "companyWorst": search_interview.companyWorst if search_interview.companyName else None
#             } for search_interview in search_interviews],
#             "total": len(job_interviews)
#         }
#
#     return render_template("interviewlist.html", response = response)


@interview_bp.route('/list') # 모의면접 목록 페이지.
def interviewlist_company():
    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))
    job_interviews, company_interviews, job_total, company_total = InterviewService.get_interview_list()
    response = {
        "interviews" : [{
                "interviewId" : company_interview.interviewId,
                "companyName" : company_interview.companyName,
                "level" : company_interview.level,
                "title" : company_interview.title,
                "jobName" : company_interview.jobName, # 지원 분야
                "university": company_interview.university, # 출신 학교
                "companyBest": [company_best.content for company_best in company_interview.companyBest],
                "companyWorst": company_interview.companyWorst
            } for company_interview in company_interviews],
        "total" :company_total
    }
    print(response)
    return render_template("interviewlist.html", response = response)


@interview_bp.route('/list/job') # 모의면접 목록 페이지.
def interviewlist_job():
    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    job_interviews, company_interviews, job_total,company_total = InterviewService.get_interview_list()

    response = {
        "interviews": [{
            "occupationId": job_interview['occupationId'],
            "occupationName": job_interview['occupationName'],
            "competencies": job_interview['competencies'],
            "interviews": [{
                "interviewId": interview.interviewId,
                "level": interview.level,
                "title": interview.title,
                "jobName": interview.jobName,  # 지원 분야
                "university": interview.university  # 출신 학교
             } for interview in job_interview['jobInterviews']],
            "total": job_interview['total']
        } for job_interview in job_interviews],
        "total" : job_total
    }
    print(response)
    return render_template("interview_job.html", response = response)


@interview_bp.route('/list/search') # 모의면접 목록 페이지.
def interviewlist_search():
    #jwt_factory = JWTFactory()
    #user_id = jwt_factory.verify_access_token(request.cookies.get('access_token'))

    keyword = request.args.get('keyword', None, type=str)

    if keyword is None :
        search_interviews, total = [], 0
    else :
        search_interviews, total = InterviewService.get_interview_list_search(keyword)
    response = {
        "interviews": [{
            "interviewId": search_interview.interviewId,
            "companyName": search_interview.companyName,
            "level": search_interview.level,
            "title": search_interview.title,
            "jobName": search_interview.jobName,  # 지원 분야
            "university": search_interview.university,  # 출신 학교
            "companyBest": [company_best.content for company_best in search_interview.companyBest] if search_interview.companyName else None,
            "companyWorst": search_interview.companyWorst if search_interview.companyName else None
        } for search_interview in search_interviews],
        "total": total
    }
    return render_template("interview_search.html", response = response)


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

@interview_bp.route('/make/company')
def make_company():
    make_company_improvement()
    return render_template("resume_loading.html.html")

