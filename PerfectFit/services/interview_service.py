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
        interviews = get_session().query(Interview).filter(Interview.resume_id == resume_id).all()

        questions = []

        for interview in interviews:
            interview_questions: list[InterviewQuestion] = get_session().query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview.interview_id).all()
            for interview_question in interview_questions:
                questions.append(InterviewDto.Response.interviewQuestion(interview_question.question_id,interview_question.question))
        # if not jobs :
        #     raise CustomException(ExceptionType.NOT_FOUND_JOB)
        return questions

    @staticmethod
    def post_question_answer(question_answer: InterviewDto.Request.postInterviewAnswer) -> None:
        interview_answer: InterviewAnswer = InterviewAnswer(question_id=question_answer.questionId, answer=question_answer.answer)

        get_session().add(interview_answer)
        get_session().commit()

    # questionId: int
    # title: str
    # answer: str
    # isPublic: bool
    @staticmethod
    def get_is_public(interview_id: int) -> list[InterviewDto.Response.isPublicInterview] :
        questions: list[InterviewQuestion] = get_session().query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).all()
        isPublicInterviews = []
        for question in questions:
            isPublicInterviewDto = InterviewDto.Response.isPublicInterview(question.question_id, question.question, question.interview_answers.answer, question.is_shared)
            isPublicInterviews.append(isPublicInterviewDto)
        return isPublicInterviews