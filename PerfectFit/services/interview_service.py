from typing import Tuple, Any, List

import celery
from sqlalchemy import func, desc
from flask import current_app, flash

from config.config_mysql import get_session
from domain.models import ResumeView, ResumeLike, InterviewImprovement, Company, AppUser, Job, CompanyBest, \
    CompanyWorst, Occupation, InterviewView, InterviewLike, InterviewAnswer
from domain.models.competencies import Competencies
from dto.company_best.company_best import CompanyBestDto
from dto.resume.resume import ResumeDto

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from dto.interview.interview import InterviewDto

from domain.models.interview import Interview
from domain.models.interview_question import InterviewQuestion
from tasks import start_async_ai_task, add_resume_task
from utils.celery_util import update_task_status, create_task, generate_unique_task_id

from utils.open_ai import answer_improvement, make_interview_based_on_resume, make_interview_based_on_job

from hanspell import spell_checker

from celery import Celery
class InterviewService:

    @staticmethod
    def get_questions(interview_id: int) -> InterviewDto.Response.Questions:
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

            response: InterviewDto.Response.Questions = InterviewDto.Response.Questions(
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
        job_total = 0
        company_total = 0

        with get_session() as session:
            occupations = (
                session
                .query(Occupation)
                .all()
            )
            job_interviews = [
                {"occupationId":occupation.occupation_id,
                 "occupationName": occupation.occupation_name,
                 "competencies": [ coms.content  for coms in session.query(Competencies).filter(Competencies.occupation_id == occupation.occupation_id).all()],
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

            interviews: List[Interview] = (
                session
                .query(Interview)
                .filter(Interview.interview_id.in_(
                    session.query(InterviewQuestion.interview_id)
                    .filter(InterviewQuestion.is_shared == True)
                ))
                .all()
            )

            for interview in interviews:

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
                        companyName=company_name,
                        level=interview.level,
                        title=interview.title,
                        jobName=job.job_name,
                        university=user.university,
                        companyBest= [CompanyBestDto.Response.CompanyBest(
                            companyBestId=company_best.company_id,
                            content=company_best.content)
                            for company_best in company_bests[:2]],
                        companyWorst= company_worst.content)

                    company_interviews.append(company_interview)
                    company_total += 1

                job_interview = InterviewDto.Response.JobInterviewResponse(
                    interviewId=interview.interview_id,
                    companyName=company_name if company_name is not None else None,
                    level=interview.level,
                    title=interview.title,
                    jobName=job.job_name,
                    university=user.university
                    )

                for job_entry in job_interviews:
                    if job_entry["occupationId"] == job.occupation_id:
                        job_entry["jobInterviews"].append(job_interview)
                        job_entry["total"] += 1
                        job_total += 1
                        break

            session.close()
            return job_interviews, company_interviews, job_total, company_total

    def get_interview_list_search(keyword: str):
        response = []
        with get_session() as session:

            interviews: List[Interview] = (
                session
                .query(Interview)
                .filter(Interview.interview_id.in_(
                    session.query(InterviewQuestion.interview_id)
                    .filter(
                        InterviewQuestion.is_shared == True,
                        InterviewQuestion.question.like(f"%{keyword}%")  # LIKE 조건 추가
                    )
                ))
                .all()
            )
            total = 0

            for interview in interviews:
                print(interview)
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
                        companyName=company_name,
                        level=interview.level,
                        title=interview.title,
                        jobName=job.job_name,
                        university=user.university,
                        companyBest= [CompanyBestDto.Response.CompanyBest(
                            companyBestId=company_best.company_id,
                            content=company_best.content)
                            for company_best in company_bests[:2]],
                        companyWorst= company_worst.content)

                    response.append(search_interview)
                else :
                    search_interview = InterviewDto.Response.CompanyInterviewResponse(
                        interviewId=interview.interview_id,
                        companyName=company_name if company_name is not None else None,
                        level=interview.level,
                        title=interview.title,
                        jobName=job.job_name,
                        university=user.university,
                        companyBest=None,
                        companyWorst=None)

                    response.append(search_interview)
                total += 1

            session.close()
            return response, total
    @staticmethod
    def post_question_answer(question_answer: InterviewDto.Request.PostInterviewAnswer, user_id: int) -> None:
        from app import app  # Flask 애플리케이션 가져오기
        with app.app_context():  # Flask 애플리케이션 컨텍스트 활성화
            session = get_session()
            print("!")
            task_id = None
            questions = []
            best_answers = []
            try:
                # 상태 저장 (PENDING)
                print("2")

                for question_id in question_answer.questionIds :
                    question = session.query(InterviewQuestion).filter_by(question_id=question_id).first()
                    best_answer = session.query(InterviewAnswer).filter_by(question_id=question_id).first()
                    questions.append(question.question)
                    best_answers.append(best_answer.answer)

                print("3")
                print("user_answers :: ", question_answer.answers)
                print("question_ids :: ", question_answer.questionIds)
                print("questions :: ", questions)
                print("best_answers :: ", best_answers)
                # 비동기 AI 작업 시작
                async_result = start_async_ai_task.apply_async(kwargs={
                    "user_answers":question_answer.answers,
                    "question_ids":question_answer.questionIds,
                    "questions":questions,
                    "best_answers":best_answers})

                print("3a2")
                # improvements = async_result.get(timeout=30)
                #
                # for improvement in improvements['InterviewImprovement']:
                #     new_improvement = InterviewImprovement(
                #         question_id=int(question_answer.questionId),
                #         answer=improvement['UserAnswer'],
                #         improvement=improvement['Improvement'],
                #         translated_answer=improvement['TranslatedAnswer']
                #     )
                #     session.add(new_improvement)
                session.commit()

                print("석세스")

                # 작업 ID 반환
                return async_result
            except Exception as e:
                session.rollback()
                if task_id is not None :
                    update_task_status(task_id, status='FAILED')
                print("Exception Cause2 ::", e)
                raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)

    @staticmethod
    def post_question_answer_after(task_id: str):
        with get_session() as session:
            task = start_async_ai_task.AsyncResult(task_id)
            improvements = task.get()
            print(improvements)
            for interview_improvement in improvements:
                improvement = interview_improvement['InterviewImprovement']
                new_improvement = InterviewImprovement(
                    question_id=improvement['questionId'],
                    answer=improvement['UserAnswer'],
                    improvement=improvement['Improvement'],
                    translated_answer=improvement['TranslatedAnswer']
                )
                session.add(new_improvement)
            # 상태 업데이트 (COMPLETED)
            # update_task_status(task_id, status='COMPLETED')
            session.commit()


    @staticmethod
    def make_interview_resume(request_dto: InterviewDto.Request.PostMakeInterviewResume) -> None:
        session = get_session()

        try:
            interview_id = make_interview_based_on_resume(request_dto.resumeId, request_dto.level, request_dto.title)
            return interview_id
        except Exception as e:
            session.rollback()
            print("Exception Cause2 :: ", e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)

    @staticmethod
    def make_interview_job(request_dto: InterviewDto.Request.PostMakeInterviewJob) -> None:
        session = get_session()

        try:
            interview_id = make_interview_based_on_job(request_dto.jobId,request_dto.userId, request_dto.level, request_dto.title)
            return interview_id
        except Exception as e:
            session.rollback()
            print("Exception Cause2 :: ", e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)


    @staticmethod
    def patch_interview_title(interview_title: InterviewDto.Request.PatchInterviewTitle) -> None:

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
    def get_is_public(interview_id: int) -> list[InterviewDto.Response.IsPublicInterview] :
        questions: list[InterviewQuestion] = get_session().query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).all()
        isPublicInterviews = []

        if not questions :
            raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

        for question in questions:
            for answer in question.interview_answers :
                isPublicInterviewDto = InterviewDto.Response.IsPublicInterview(question.question_id, question.question, answer .answer, question.is_shared)
                isPublicInterviews.append(isPublicInterviewDto)

        return isPublicInterviews

    @staticmethod
    def get_improvement(task_id: int, user_id: int) -> list[InterviewDto.Response.Improvement] :

        with get_session() as session :

            task = start_async_ai_task.AsyncResult(task_id)

            if task is None:
                flash("Celery 작업에 문제가 생겼습니다.")
                return None

            question_id = task.get()[0]['InterviewImprovement']['questionId']

            question = session.query(InterviewQuestion).filter_by(question_id=question_id).first()
            interview_id = question.interview_id

            interview:Interview = session.query(Interview).filter_by(interview_id=interview_id).first()
            questions: list[InterviewQuestion] = session.query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).order_by(desc(InterviewQuestion.created_time)).limit(10).all()
            improvementList = []

            if not questions :
                raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

            for question in questions:
                improvement = session.query(InterviewImprovement).filter(InterviewImprovement.question_id == question.question_id).order_by(desc(InterviewImprovement.created_time)).first()

                if improvement :
                    if (improvement.question.interview.user_id == user_id) or \
                            (improvement.question.interview.user_id != user_id and \
                             improvement.question.is_shared == True):
                        improvementDto = InterviewDto.Response.Improvement(
                            improvementId = improvement.improvement_id,
                            questionId = question.question_id,
                            question = question.question,
                            answer = improvement.answer,
                            improvement = improvement.improvement,
                            translatedAnswer = improvement.translated_answer)
                        improvementList.append(improvementDto)

            view = session.query(InterviewView).filter_by(user_id=user_id).first()

            if view is None:
                new_view = InterviewView(interview_id=interview_id, company_id=interview.company_id, user_id=user_id)
                session.add(new_view)
                session.commit()

            return improvementList
    @staticmethod
    def get_improvement_based_id(interview_id: int, user_id: int) -> list[InterviewDto.Response.Improvement] :
        with (get_session() as session) :
            interview:Interview = session.query(Interview).filter_by(interview_id=interview_id).first()
            questions: list[InterviewQuestion] = session.query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).order_by(desc(InterviewQuestion.created_time)).limit(10).all()
            improvementList = []

            if not questions :
                raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

            for question in questions:
                improvement = session.query(InterviewImprovement).filter(InterviewImprovement.question_id == question.question_id).order_by(desc(InterviewImprovement.created_time)).first()

                if improvement :
                    if (improvement.question.interview.user_id == user_id) or \
                        (improvement.question.interview.user_id != user_id and \
                         improvement.question.is_shared == True) :
                        improvementDto = InterviewDto.Response.Improvement(
                            improvementId = improvement.improvement_id,
                            questionId = question.question_id,
                            question = question.question,
                            answer = improvement.answer,
                            improvement = improvement.improvement,
                            translatedAnswer = improvement.translated_answer)
                        improvementList.append(improvementDto)

            view = session.query(InterviewView).filter_by(user_id=user_id).first()

            if view is None:
                new_view = InterviewView(interview_id=interview_id, company_id=interview.company_id, user_id=user_id)
                session.add(new_view)
                session.commit()

            return improvementList
    @staticmethod
    def get_interview_title(question_id: int, interview_id: int):
        with get_session() as session :
            if interview_id is None :
                question = session.query(InterviewQuestion).filter_by(question_id=question_id).first()
                interview = session.query(Interview).filter_by(interview_id=question.interview_id).first()
                return interview.title, question.interview_id
            else :
                interview = session.query(Interview).filter_by(interview_id=interview_id).first()
                return interview.title, interview.interview_id
    @staticmethod
    def get_question_is_shared(question_id: int):
        with get_session() as session :
            if question_id is not None :
                question = session.query(InterviewQuestion).filter_by(question_id=question_id).first()
                return question.is_shared

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
    def spell_check(spellCheckDto: InterviewDto.Request.SpellCheck) -> str:
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
    def get_interviews(user_id: int, page: int, count: int) -> tuple[list[InterviewDto.Response.InterviewSummary], int]:
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

            summary = InterviewDto.Response.InterviewSummary(
                interview_id=interview.interview_id,
                title=interview.title,
                created_time=interview.created_time,
                view_count=view_count,
                like_count=like_count,
            )
            interview_summaries.append(summary)

        return interview_summaries, total
