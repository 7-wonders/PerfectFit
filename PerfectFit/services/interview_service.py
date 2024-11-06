from flask import flash, abort
from flask_sqlalchemy.pagination import Pagination

from database.config import get_session
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from dto.interview.interview import InterviewDto
from domain.models.interview import Interview
from domain.models.interview_question import InterviewQuestion
from domain.models.interview_answer import InterviewAnswer

class InterviewService:

    @staticmethod
    def get_questions(resume_id: int) -> list[InterviewDto.Response.interviewQuestion]:
        # join을 해서 results에 일단 담기
        results = (
            get_session()
            .query(InterviewQuestion)
            .join(Interview, InterviewQuestion.interview_id == Interview.interview_id)
            .filter(Interview.resume_id == resume_id)
            .all()
        )

        questions = [
            InterviewDto.Response.interviewQuestion(question.question_id, question.question)
            for question in results
        ]

        if not questions :
            raise CustomException(ExceptionType.NOT_FOUND_QUESTION)
        return questions

    @staticmethod
    def post_question_answer(question_answer: InterviewDto.Request.postInterviewAnswer) -> None:
        interview_answer: InterviewAnswer = InterviewAnswer(question_id=question_answer.questionId, answer=question_answer.answer)

        try:
            get_session().add(interview_answer)
            get_session().commit()
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
    def get_improvement(interview_id: int) -> list[InterviewDto.Response.improvement] :
        questions: list[InterviewQuestion] = get_session().query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).all()
        improvementList = []

        if not questions :
            raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

        for question in questions:
            for improvement in question.interview_improvements :
                if improvement :
                    improvementDto = InterviewDto.Response.improvement(improvement.improvement_id, question.question_id, improvement.answer, improvement.improvement)
                    improvementList.append(improvementDto)
        return improvementList