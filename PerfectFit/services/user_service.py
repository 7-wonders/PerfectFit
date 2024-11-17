from flask_sqlalchemy.pagination import Pagination
from sqlalchemy.orm import joinedload
from domain.models.app_user import AppUser
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from config.config_mysql import get_session


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