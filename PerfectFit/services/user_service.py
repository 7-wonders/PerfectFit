from flask import flash, abort
from flask_sqlalchemy.pagination import Pagination

from database.config import get_session
from domain.models.app_user import AppUser
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType


class UserService:
    @staticmethod
    def get_users(page: int, count: int) -> Pagination:
        paginate_user = AppUser.query.paginate(page=page, per_page=count, error_out=False)
        return paginate_user

    @staticmethod
    def get_user(user_id: int) -> AppUser | None:
        user: AppUser = get_session().query(AppUser).filter( ##
            AppUser.user_id == user_id
        ).first()
        user.project_experience ## 이거 변수에 담아야 함 SQL Alchemy 관계설정

        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        return user














