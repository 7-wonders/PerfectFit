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
        user = get_session().query(AppUser).filter(
            AppUser.user_id == user_id
        ).first()

        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        return user
