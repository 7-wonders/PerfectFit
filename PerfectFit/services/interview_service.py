from flask import flash, abort
from flask_sqlalchemy.pagination import Pagination

from database.config import get_session
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from dto.interview.interview import InterviewDto
from domain.models.interview import Interview
from domain.models.interview_question import InterviewQuestion
from domain.models.interview_answer import InterviewAnswer

from hanspell import spell_checker
import re, requests

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

    @staticmethod
    def spell_check(spellCheckDto: InterviewDto.Request.spellCheck) -> str:
        text = spellCheckDto.content

        try:
            passportKey = get_passport_key()

            # 맞춤법 검사 수행
            result = spell_checker.check(text, passportKey)
            print(result)
            print(result.checked)
            return result.checked
        except Exception as e:
            print("Error occurred:", e)


def get_passport_key():
    """네이버에서 '네이버 맞춤법 검사기' 페이지에서 passportKey를 획득

        - 네이버에서 '네이버 맞춤법 검사기'를 띄운 후
        html에서 passportKey를 검색하면 값을 찾을 수 있다.

        - 찾은 값을 spell_checker.py 48 line에 적용한다.
    """

    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=네이버+맞춤법+검사기"
    res = requests.get(url)

    html_text = res.text

    match = re.search(r'passportKey=([^&"}]+)', html_text)
    if match:
        passport_key = match.group(1)
        return passport_key
    else:
        return False
