from flask import flash, abort
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy.orm import joinedload

from database.config import get_session
from domain.models import ResumeLike
from domain.models.app_user import AppUser
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType

from sqlalchemy.sql import func
from domain.models.resume import Resume
from domain.models.resume_view import ResumeView


class UserService:
    @staticmethod
    def get_users(page: int, count: int) -> Pagination:
        paginate_user = AppUser.query.paginate(page=page, per_page=count, error_out=False)
        return paginate_user

    @staticmethod
    def get_user(user_id: int) -> AppUser | None:
        user: AppUser = get_session().query(AppUser).options(
            joinedload(AppUser.project_experience)
        ).filter(AppUser.user_id == user_id).first()

        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        # project_experience를 변수에 담기
        project_experiences = user.project_experience  # SQLAlchemy 관계로 가져온 데이터

        return user

class ResumeService:
    @staticmethod
    def get_resumes(user_id: int, page: int, count: int):
        session = get_session()

        # 자기소개서 목록을 가져오기 위한 쿼리
        resumes_query = session.query(Resume).filter(Resume.user_id == user_id)
        total = resumes_query.count()

        resumes = resumes_query.order_by(Resume.created_time.desc()) \
                               .offset((page - 1) * count) \
                               .limit(count) \
                               .all()

        # 조회수 및 좋아요 수 계산
        for resume in resumes:
            resume.view_count = session.query(func.sum(ResumeView.view_count)).filter(
                ResumeView.resume_id == resume.resume_id
            ).scalar() or 0

            resume.like_count = session.query(func.sum(ResumeLike.like_count)).filter(
                ResumeLike.resume_id == resume.resume_id
            ).scalar() or 0

        return resumes, total














