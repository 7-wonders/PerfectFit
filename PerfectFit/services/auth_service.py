from typing import Optional, cast

from flask import request
from flask_sqlalchemy.session import Session
from sqlalchemy.orm import scoped_session

from constants.sns_kind import SnsKind
from config.config_mysql import get_session
from domain.models import AppUser, ProjectExperience, ProjectExperienceTask, WorkExperience
from dto.user.user import UserDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from utils.age import get_age
from utils.jwt_factory import JWTFactory
from utils.oauth.google_oauth_handler import GoogleOAuthHandler
from utils.oauth.kakao_oauth_handler import KakaoOAuthHandler
from utils.oauth.naver_oauth_handler import NaverOAuthHandler

logger = Logger('auth_service')


def _check_enough_info(sns_id: str, name: str) -> bool:
    if not sns_id or not name:
        return False

    return True


def _create_token(user_id: int) -> dict:
    jwt_factory = JWTFactory()
    return jwt_factory.create_token(user_id)


def _delete_refresh_token():
    refresh_token = request.cookies.get('refresh_token')

    if not refresh_token:
        return

    jwt_factory = JWTFactory()
    jwt_factory.delete_refresh_token(refresh_token)


class AuthService:
    @staticmethod
    def google_login(code: str) -> tuple[UserDto.Request.Signup | dict, bool]:
        with get_session() as session:
            access_token, token_type = GoogleOAuthHandler().get_access_token(code)
            user_response_json = GoogleOAuthHandler().get_user_info(token_type, access_token)

            sns_id = user_response_json.get('id')
            email = user_response_json.get('email')
            name = user_response_json.get('name')
            profile_image = user_response_json.get('picture')

            if not _check_enough_info(sns_id, name):
                logger.error(f'User Request Error\n'
                             f'sns_id : {sns_id} | email : {email} | name : {name}')
                raise CustomException(ExceptionType.GOOGLE_NOT_ENOUGH_INFO)

            already_user: Optional[AppUser] = session.query(AppUser).filter(AppUser.sns_id == sns_id).first()
            if already_user:
                _delete_refresh_token()
                return _create_token(already_user.user_id), True

            logger.info(f'Google Signup Success\n'
                        f'sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image}')

            return UserDto.Request.Signup(
                snsId=sns_id,
                snsKind=SnsKind.GOOGLE.value,
                username=name,
                email=email,
                profilePath=profile_image,
            ), False

    @staticmethod
    def naver_login(code: str, state: str) -> tuple[UserDto.Request.Signup | dict, bool]:
        with get_session() as session:
            session = cast(scoped_session[Session], session)

            access_token, token_type = NaverOAuthHandler().get_access_token(code, state=state)
            user_response_json = NaverOAuthHandler().get_user_info(token_type, access_token)

            sns_id = user_response_json.get('response').get('id')
            name = user_response_json.get('response').get('name')
            email = user_response_json.get('response').get('email')
            profile_image = user_response_json.get('response').get('profile_image')
            phone_number = str(user_response_json.get('response').get('mobile')).replace('-', '')

            if not _check_enough_info(sns_id, name):
                logger.error(f'User Request Error\n'
                             f'sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image} | phone_number : {phone_number}')
                raise CustomException(ExceptionType.NAVER_NOT_ENOUGH_INFO)

            already_user = session.query(AppUser).filter(AppUser.sns_id == sns_id).first()
            if already_user:
                _delete_refresh_token()
                return _create_token(already_user.user_id), True

            # MM-DD 형식
            response_birthday = user_response_json.get('response').get('birthday')
            birth_year = user_response_json.get('response').get('birthyear')
            birth_month, birth_day = map(int, response_birthday.split('-'))
            age = get_age(int(birth_year), birth_month, birth_day)

            logger.info(f'Naver Signup Success\n'
                        f'sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image} | phone_number : {phone_number} | age : {age}')

            return UserDto.Request.Signup(
                snsId=sns_id,
                snsKind=SnsKind.NAVER.value,
                username=name,
                email=email,
                phoneNumber=phone_number,
                profilePath=profile_image,
                age=age,
            ), False

    @staticmethod
    def kakao_login(code: str, state: str) -> tuple[UserDto.Request.Signup | dict, bool]:
        with get_session() as session:
            access_token, token_type = KakaoOAuthHandler().get_access_token(code, state=state)
            user_response_json = KakaoOAuthHandler().get_user_info(token_type, access_token)

            sns_id = user_response_json.get('id')
            name = user_response_json.get('properties').get('nickname')
            profile_image = user_response_json.get('properties').get('profile_image')

            if not _check_enough_info(sns_id, name):
                logger.error(f'User Request Error\n'
                             f'sns_id : {sns_id} | name : {name} | profile_image : {profile_image}')
                raise CustomException(ExceptionType.KAKAO_NOT_ENOUGH_INFO)

            already_user = session.query(AppUser).filter(AppUser.sns_id == sns_id).first()

            if already_user:
                _delete_refresh_token()
                return _create_token(already_user.user_id), True

            logger.info(f'Kakao Signup Success\n'
                        f'sns_id : {sns_id} | name : {name} | profile_image : {profile_image}')

            return UserDto.Request.Signup(
                snsId=sns_id,
                snsKind=SnsKind.KAKAO.value,
                username=name,
                profilePath=profile_image,
            ), False

    @staticmethod
    def renew_token(refresh_token: str) -> dict:
        jwt_factory = JWTFactory()
        token_info = jwt_factory.renew_token(refresh_token)
        _delete_refresh_token()

        return token_info

    @staticmethod
    def signup(
            major: str, university: str, university_status: str, grade: str, phone_number: str,
            project_experiences: list, work_experiences: list,
            info: UserDto.Response.NecessaryInfo
    ):
        with get_session() as session:
            user = AppUser(
                sns_kind=info['snsKind'],
                sns_id=info['snsId'],
                username=info['username'],
                email=info['email'],
                age=info['age'],
                address=info['address'],
                detail_address=info['detailAddress'],
                profile_path=info['profilePath'] or None,
                major=major,
                university=university,
                university_status=university_status,
                grade=grade,
                phone_number=phone_number,
            )

            session.add(user)
            session.flush()

            for project in project_experiences:
                new_project = ProjectExperience(
                    user_id=user.user_id,
                    project_name=project['projectName'],
                    from_date=project['fromDate'],
                    to_date=project['toDate'],
                )

                session.add(new_project)
                session.flush()

                for content in project['contents']:
                    new_task = ProjectExperienceTask(
                        project_experience_id=new_project.project_experience_id,
                        content=content,
                    )
                    session.add(new_task)

            for work in work_experiences:
                new_work = WorkExperience(
                    user_id=user.user_id,
                    company_name=work['companyName'],
                    position=work['position'],
                    from_date=work['fromDate'],
                    to_date=work['toDate'],
                    reason=work['reason'],
                    responsibility=work['responsibility'],
                )
                session.add(new_work)

            session.commit()

            return _create_token(user.user_id)
