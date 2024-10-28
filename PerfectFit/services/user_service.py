from flask import flash
from flask_sqlalchemy.pagination import Pagination

from database.config import db
from domain.models.app_user import AppUser


class UserService:
    @staticmethod
    def get_users(page: int, count: int) -> Pagination:
        try:
            paginate_user = AppUser.query.paginate(page=page, per_page=count, error_out=False)
            return paginate_user
        except Exception as e:
            print(f"Error fetching users: {e}")  # 에러 발생 시 메시지 출력
            flash("예기치 못한 에러가 발생하였습니다.", "error")
            return None

    @staticmethod
    def get_user(user_id: int) -> AppUser | None:
        try:
            user = db.get_or_404(AppUser, user_id)

            if not user:
                return None

            return user
        except Exception as e:
            print(f"Error fetching user : {e}")
            flash("예기치 못한 에러가 발생하였습니다.", "error")
            return None
