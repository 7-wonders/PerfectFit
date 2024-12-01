import celery
from sqlalchemy import func

from config.config_mysql import get_session
from domain.models import ResumeView, ResumeLike, InterviewImprovement, Company, AppUser, Job, CompanyBest, \
    CompanyWorst, Occupation, InterviewView, InterviewLike
from dto.company_best.company_best import CompanyBestDto
from dto.resume.resume import ResumeDto

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from dto.interview.interview import InterviewDto

from domain.models.interview import Interview
from domain.models.interview_question import InterviewQuestion
from tasks import start_async_ai_task, add_resume_task
from utils.celery_util import update_task_status, create_task

from utils.open_ai import answer_improvement, make_interview_based_on_resume, make_interview_based_on_job

from hanspell import spell_checker

from celery import Celery
class InterviewService:

    @staticmethod
    def get_questions(interview_id: int) -> InterviewDto.Response.questions:
        with get_session() as session:
            # join을 해서 results에 일단 담기
            results = (
                session
                .query(InterviewQuestion)
                .join(Interview, InterviewQuestion.interview_id == Interview.interview_id)
                .filter(Interview.interview_id == interview_id)
                .all()
            )

            questions = [
                InterviewDto.Response.InterviewQuestion(question.interview_id, question.question_id, question.question)
                for question in results
            ]

            if not questions:
                raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

            response: InterviewDto.Response.questions = InterviewDto.Response.questions(
                questions=
                [InterviewDto.Response.InterviewQuestion(question.interview_id, question.question_id, question.question)
                 for question in questions],
                total=len(questions)
            )

            session.close()

        return response

    @staticmethod
    def get_interview_list():
        """
        1. 인터뷰 질문 공유 true인 것 전부 들고오기
        2. 인터뷰 질문 하나씩 for문 돌리기
        3. JobInterviews에는 무조건 넣고, CompanyInterviews에는 Company가 있다면 넣기
        4
            companyName: str # company 테이블 참조
            level: str # interview
            title: str # interview
            jobName: str # job 테이블 참조
            university: str # app_user에서 참조
            companyBest: list[CompanyBestDto.Response.CompanyBest] # company_best에서 참조
            companyWorst: str # company_worst에서 참조
        :return:
        """
        company_interviews = []


        with get_session() as session:
            occupations = (
                session
                .query(Occupation)
                .all()
            )

            job_interviews = [
                {"occupationId":occupation.occupation_id,
                 "jobInterviews": [],
                 "total": 0} for occupation in occupations
            ]

            results = (
                session
                .query(InterviewQuestion)
                .filter(InterviewQuestion.is_shared == True)
                .all()
            )

            questions = [
                InterviewDto.Response.InterviewQuestion(question.interview_id, question.question_id, question.question)
                for question in results
            ]

            if not questions:
                raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

            for question in questions:
                interview:Interview = (
                    session
                    .query(Interview)
                    .filter(Interview.interview_id == question.interview_id)
                    .first()
                )

                user:AppUser= (
                    session
                    .query(AppUser)
                    .filter(AppUser.user_id == interview.user_id)
                    .first()
                )

                job:Job= (
                    session
                    .query(Job)
                    .filter(Job.job_id == interview.job_id)
                    .first()
                )
                company_name = None
                if interview.company_id is not None :
                    company:Company = (
                        session
                        .query(Company)
                        .filter(Company.company_id == interview.company_id)
                        .first()
                    )

                    company_bests:list[CompanyBest] = (
                        session
                        .query(CompanyBest)
                        .filter(CompanyBest.company_id == interview.company_id)
                        .all()
                    )

                    company_worst:CompanyWorst= (
                        session
                        .query(CompanyWorst)
                        .filter(CompanyWorst.company_id == interview.company_id)
                        .first()
                    )

                    company_name = company.company_name

                    company_interview = InterviewDto.Response.CompanyInterviewResponse(
                        interviewId=interview.interview_id,
                        questionId=question.question_id,
                        companyName=company_name,
                        level=interview.level,
                        title=interview.title,
                        jobName=job.job_name,
                        university=user.university,
                        companyBest= [CompanyBestDto.Response.CompanyBest(
                            companyBestId=company_best.company_id,
                            content=company_best.content)
                            for company_best in company_bests],
                        companyWorst= company_worst.content)

                    company_interviews.append(company_interview)

                job_interview = InterviewDto.Response.JobInterviewResponse(
                    interviewId=interview.interview_id,
                    questionId=question.question_id,
                    companyName=company_name if company_name is not None else None,
                    level=interview.level,
                    title=interview.title,
                    jobName=job.job_name,
                    university=user.university)

                for job_entry in job_interviews:
                    if job_entry["occupationId"] == job.occupation_id:
                        job_entry["jobInterviews"].append(job_interview)
                        job_entry["total"] += 1
                        break

            session.close()
            return job_interviews, company_interviews

    def get_interview_list_search(keyword: str):
        interviews = []

        with get_session() as session:
            occupations = (
                session
                .query(Occupation)
                .all()
            )

            results = (
                session
                .query(InterviewQuestion)
                .filter(
                    InterviewQuestion.is_shared == True,
                    InterviewQuestion.question.like(f'%{keyword}%'))
                .all()
            )

            questions = [
                InterviewDto.Response.InterviewQuestion(question.interview_id, question.question_id, question.question)
                for question in results
            ]

            if not questions:
                raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

            for question in questions:
                interview:Interview = (
                    session
                    .query(Interview)
                    .filter(Interview.interview_id == question.interview_id)
                    .first()
                )

                user:AppUser= (
                    session
                    .query(AppUser)
                    .filter(AppUser.user_id == interview.user_id)
                    .first()
                )

                job:Job= (
                    session
                    .query(Job)
                    .filter(Job.job_id == interview.job_id)
                    .first()
                )

                company_name = None

                if interview.company_id is not None :
                    company:Company = (
                        session
                        .query(Company)
                        .filter(Company.company_id == interview.company_id)
                        .first()
                    )

                    company_bests:list[CompanyBest] = (
                        session
                        .query(CompanyBest)
                        .filter(CompanyBest.company_id == interview.company_id)
                        .all()
                    )

                    company_worst:CompanyWorst= (
                        session
                        .query(CompanyWorst)
                        .filter(CompanyWorst.company_id == interview.company_id)
                        .first()
                    )

                    company_name = company.company_name

                    search_interview = InterviewDto.Response.CompanyInterviewResponse(
                        interviewId=interview.interview_id,
                        questionId=question.question_id,
                        companyName=company_name,
                        level=interview.level,
                        title=interview.title,
                        jobName=job.job_name,
                        university=user.university,
                        companyBest= [CompanyBestDto.Response.CompanyBest(
                            companyBestId=company_best.company_id,
                            content=company_best.content)
                            for company_best in company_bests],
                        companyWorst= company_worst.content)

                    interviews.append(search_interview)
                else :
                    search_interview = InterviewDto.Response.CompanyInterviewResponse(
                        interviewId=interview.interview_id,
                        questionId=question.question_id,
                        companyName=company_name if company_name is not None else None,
                        level=interview.level,
                        title=interview.title,
                        jobName=job.job_name,
                        university=user.university,
                        companyBest=None,
                        companyWorst=None)

                    interviews.append(search_interview)


            session.close()
            return interviews
    @staticmethod
    def post_question_answer(question_answer: InterviewDto.Request.postInterviewAnswer, user_id: int) -> None:
        session = get_session()
        print("!")
        try:
            # 상태 저장 (PENDING)
            task_id = create_task(user_id, question_answer.questionId, status='PENDING')
            print("2")
            # 비동기 AI 작업 시작
            # async_result = start_async_ai_task.apply_async(kwargs={
            #     "user_answer":question_answer.answer,
            #     "question_id":question_answer.questionId,
            #     "task_id":task_id})
            job = get_session().query(Job).filter(Job.job_id == 253).first()

            async_result = add_resume_task.apply_async(kwargs={
                "job": job,
                "user": AppUser(),
                "resume": ResumeDto.Request.CreateFullResume
            })

            print("3")

            # 작업 ID 반환
            return async_result
        except Exception as e:
            session.rollback()
            print("Exception Cause2 ::", e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)


    @staticmethod
    def make_interview_resume(request_dto: InterviewDto.Request.postMakeInterviewResume) -> None:
        session = get_session()

        try:
            make_interview_based_on_resume(request_dto.resumeId, request_dto.level, request_dto.title)
        except Exception as e:
            session.rollback()
            print("Exception Cause2 :: ", e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)

    @staticmethod
    def make_interview_job(request_dto: InterviewDto.Request.postMakeInterviewJob) -> None:
        session = get_session()

        try:
            make_interview_based_on_job(request_dto.jobId,request_dto.userId, request_dto.level, request_dto.title)
            return
        except Exception as e:
            session.rollback()
            print("Exception Cause2 :: ", e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)


    @staticmethod
    def patch_interview_title(interview_title: InterviewDto.Request.patchInterviewTitle) -> None:

        try:
            session = get_session()
            interview = session.query(Interview).filter_by(interview_id=interview_title.interviewId).first()

            if interview is None:
                raise CustomException(ExceptionType.NOT_FOUND_INTERVIEW)

            interview.title = interview_title.title

            # 변경 사항 커밋
            session.commit()
        except Exception as e:
            get_session().rollback()
            print("Exception Cause :: ",e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)

    @staticmethod
    def patch_ispublic(questionIds: list[int]) -> None:

        try:
            session = get_session()

            for questionId in questionIds:
                interview_question = session.query(InterviewQuestion).filter_by(question_id=questionId).first()
                if interview_question is None:
                    raise CustomException(ExceptionType.NOT_FOUND_INTERVIEW)

                interview_question.is_shared = True

            session.commit()

        except Exception as e:
            get_session().rollback()
            print("Exception Cause :: ",e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)

    @staticmethod
    def patch_ispublic_cancel(questionIds: list[int]) -> None:

        try:
            session = get_session()

            for questionId in questionIds:
                interview_question = session.query(InterviewQuestion).filter_by(question_id=questionId).first()
                if interview_question is None:
                    raise CustomException(ExceptionType.NOT_FOUND_INTERVIEW)

                interview_question.is_shared = False

            session.commit()

        except Exception as e:
            get_session().rollback()
            print("Exception Cause :: ",e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)
    @staticmethod
    def get_is_public(interview_id: int) -> list[InterviewDto.Response.isPublicInterview] :
        questions: list[InterviewQuestion] = get_session().query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).all()
        isPublicInterviews = []

        if not questions :
            raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

        for question in questions:
            for answer in question.interview_answers :
                isPublicInterviewDto = InterviewDto.Response.isPublicInterview(question.question_id, question.question, answer .answer, question.is_shared)
                isPublicInterviews.append(isPublicInterviewDto)
        return isPublicInterviews

    @staticmethod
    def get_improvement(interview_id: int, user_id: int) -> list[InterviewDto.Response.improvement] :
        with get_session() as session :
            interview:Interview = session.query(Interview).filter_by(interview_id=interview_id).first()
            questions: list[InterviewQuestion] = session.query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).all()
            improvementList = []

            if not questions :
                raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

            for question in questions:
                for improvement in question.interview_improvements :
                    if improvement :
                        improvementDto = InterviewDto.Response.improvement(
                            improvement.improvement_id,
                            question.question_id,
                            improvement.answer,
                            improvement.improvement,
                            improvement.translated_answer)
                        improvementList.append(improvementDto)

            view = session.query(InterviewView).filter_by(user_id=user_id).first()

            if view is None:
                new_view = InterviewView(interview_id=interview_id, company_id=interview.company_id, user_id=user_id)
                session.add(new_view)
                session.commit()

            return improvementList

    @staticmethod
    def post_like(interview_id: int, user_id: int) -> None:
        with get_session() as session :
            like = session.query(InterviewLike).filter_by(user_id=user_id).first()

            if like is not None:
                raise CustomException(ExceptionType.ALREADY_LIKED)

            new_like = InterviewLike(interview_id=interview_id, user_id=user_id)
            session.add(new_like)
            session.commit()

    @staticmethod
    def delete_like(interview_id: int, user_id: int) -> None:
        with get_session() as session :
            like = session.query(InterviewLike).filter_by(user_id=user_id).first()

            if like is None:
                raise CustomException(ExceptionType.NOT_FOUND_LIKE)

            session.delete(like)
            session.commit()

    @staticmethod
    def spell_check(spellCheckDto: InterviewDto.Request.spellCheck) -> str:
        text = spellCheckDto.content

        try:
            # 맞춤법 검사 수행
            result = spell_checker.check(text)
            print("Checked Text:", result.checked)  # 수정된 텍스트
            print("Original Text:", result.original)  # 원본 텍스트
            print("Errors Found:", result.errors)  # 발견된 오류 수
            print("Corrections:", result.words)  # 각 단어의 교정 결과
            for word in result.words:
                print(word)
            return result.checked
        except Exception as e:
            print("Error occurred:", e)

    @staticmethod
    def get_interviews(user_id: int, page: int, count: int) -> tuple[list[InterviewDto.Response.interviewSummary], int]:
        session = get_session()

        # 면접 데이터를 가져오는 쿼리 정의
        interviews_query = session.query(Interview).filter(Interview.user_id == user_id)
        total = interviews_query.count()

        interviews = (
            interviews_query.order_by(Interview.created_time.desc())
            .offset((page - 1) * count)
            .limit(count)
            .all()
        )

        # 조회수 및 좋아요 수 계산
        interview_summaries = []
        for interview in interviews:
            view_count = session.query(func.sum(ResumeView.view_count)).filter(
                ResumeView.resume_id == interview.interview_id
            ).scalar() or 0

            like_count = session.query(func.sum(ResumeLike.like_count)).filter(
                ResumeLike.resume_id == interview.interview_id
            ).scalar() or 0

            summary = InterviewDto.Response.interviewSummary(
                interview_id=interview.interview_id,
                title=interview.title,
                created_time=interview.created_time,
                view_count=view_count,
                like_count=like_count,
            )
            interview_summaries.append(summary)

        return interview_summaries, total
