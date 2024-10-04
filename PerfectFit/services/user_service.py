from flask import flash

from domain.models.user import User
from utils.open_ai import get_test_llama_transformers, get_test_llama

class UserService:
    @staticmethod
    def get_users(page: int, count: int):
        try:
            paginate_user = User.query.paginate(page=page, per_page=count, error_out=False)
            return paginate_user
        except Exception as e:
            print(f"Error fetching users: {e}")  # 에러 발생 시 메시지 출력
            flash("예기치 못한 에러가 발생하였습니다.", "error")
            return None ## 에러 핸들링

    @staticmethod
    def get_user(user_id: int) -> User | None:
        try:
            user = User.query.filter(User.id == user_id).first() ##orm  first 를 붙인이유 : 유저가 하나만 있는게 맞지만, 여러개가 걸리면 첫번째걸로

            if not user:
                return None ## 걸린게 없으면 리턴 x

            return user
        except Exception as e:
            print(f"Error fetching user : {e}")
            flash("예기치 못한 에러가 발생하였습니다.", "error")
            return None
