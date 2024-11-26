from sqlalchemy import func

from config.config_mysql import get_session
from domain.models import ResumeView, ResumeLike, InterviewImprovement

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from dto.interview.interview import InterviewDto

from domain.models.interview import Interview
from domain.models.interview_question import InterviewQuestion

from utils.open_ai import answer_improvement, make_interview_based_on_resume, make_interview_based_on_job

from hanspell import spell_checker


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
                InterviewDto.Response.interviewQuestion(question.question_id, question.question)
                for question in results
            ]

            if not questions:
                raise CustomException(ExceptionType.NOT_FOUND_QUESTION)

            response: InterviewDto.Response.questions = InterviewDto.Response.questions(
                questions=
                [InterviewDto.Response.interviewQuestion(question.question_id, question.question)
                 for question in questions],
                total=len(questions)
            )

            session.close()

        return response

    @staticmethod
    def post_question_answer(question_answer: InterviewDto.Request.postInterviewAnswer) -> None:
        session = get_session()

        # QuestionId와 Answer가 넘어오는데 여기서 answer는 사용자가 작성한 답변이다.

        try:
            improvements = answer_improvement(question_answer.answer, question_answer.questionId)
            for improvement in improvements['InterviewImprovement']:
                new_improvement = InterviewImprovement(question_id=int(question_answer.questionId),
                                               answer=improvement['UserAnswer'],
                                               improvement=improvement['Improvement'],
                                               translated_answer=improvement['TranslatedAnswer'])
                session.add(new_improvement)
            session.commit()
        except Exception as e:
            session.rollback()
            print("Exception Cause2 :: ",e)
            raise CustomException(ExceptionType.INTERNAL_SERVER_ERROR)
        get_session().commit()

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
    def get_improvement(interview_id: int) -> list[InterviewDto.Response.improvement] :
        questions: list[InterviewQuestion] = get_session().query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).all()
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
        return improvementList

    @staticmethod
    def spell_check(spellCheckDto: InterviewDto.Request.spellCheck) -> str:
        text = spellCheckDto.content

        try:
            # 맞춤법 검사 수행
            result = spell_checker.check(text)
            print(result)
            print(result.checked)
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
