from flask import request
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy.orm import joinedload
from sqlalchemy.testing.pickleable import User

from domain.models import Resume
from domain.models.app_user import AppUser
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from config.config_mysql import get_session
from utils.jwt_factory import JWTFactory


class UserService:
    @staticmethod
    def get_users(page: int, count: int) -> Pagination:
        paginate_user = AppUser.query.paginate(page=page, per_page=count, error_out=False)
        return paginate_user

    @staticmethod
    def get_user() -> AppUser | None:
        # 이렇게 사용하면 좀 더 쉽게 사용하실 수 있습니다 !
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        user: AppUser = get_session().query(AppUser).options(
            joinedload(AppUser.project_experiences)
        ).filter(AppUser.user_id == user_id).first()

        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        return user

    @staticmethod
    def delete_user(user_id: int):
        session = get_session()

        # 사용자 조회
        user = session.query(AppUser).filter(AppUser.user_id == user_id).first()
        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        # 사용자 삭제 (Hard Delete)
        session.delete(user)
        session.commit()

    @staticmethod
    def get_user_with_resumes(page: int, count: int):
        """
        사용자 정보와 이력서를 함께 가져오는 메서드
        """
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        # 사용자 정보 및 페이징 처리된 이력서 데이터를 한 번의 쿼리로 가져오기
        user = AppUser.query.filter_by(user_id=user_id).first()
        if not user:
            raise ValueError("사용자를 찾을 수 없습니다.")

        resumes_query = Resume.query.filter_by(user_id=user_id).paginate(page=page, per_page=count)
        return user, resumes_query.items, resumes_query.total
