from typing import Optional, cast

from flask import request
from flask_sqlalchemy.session import Session
from sqlalchemy.orm import scoped_session

from constants.sns_kind import SnsKind
from config.config_mysql import get_session
from domain.models import AppUser
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
    def google_login(code: str) -> dict:
        with get_session() as session:
            session = cast(scoped_session[Session], session)
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
                return _create_token(already_user.user_id)

            user = AppUser(sns_id=sns_id, sns_kind=SnsKind.GOOGLE.value, email=email, username=name,
                           profile_path=profile_image)
            session.add(user)
            session.flush()

            logger.info(f'Google Signup Success\n'
                        f'sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image}')

            token_info = _create_token(user.user_id)
            _delete_refresh_token()

            session.commit()

            return token_info

    @staticmethod
    def naver_login(code: str, state: str) -> dict:
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
                return _create_token(already_user.user_id)

            # MM-DD 형식
            response_birthday = user_response_json.get('response').get('birthday')
            birth_year = user_response_json.get('response').get('birthyear')
            birth_month, birth_day = map(int, response_birthday.split('-'))
            age = get_age(int(birth_year), birth_month, birth_day)

            user = AppUser(sns_id=sns_id, sns_kind=SnsKind.NAVER.value, email=email, username=name,
                           profile_path=profile_image, phone_number=phone_number, age=age)
            session.add(user)
            session.flush()

            logger.info(f'Naver Signup Success\n'
                        f'sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image} | phone_number : {phone_number} | age : {age}')

            token_info = _create_token(user.user_id)
            _delete_refresh_token()

            session.commit()

            return token_info

    @staticmethod
    def kakao_login(code: str, state: str) -> dict:
        with get_session() as session:
            session = cast(scoped_session[Session], session)

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
                return _create_token(already_user.user_id)

            user = AppUser(sns_id=sns_id, sns_kind=SnsKind.KAKAO.value, username=name, profile_path=profile_image)
            session.add(user)
            session.flush()

            logger.info(f'Kakao Signup Success\n'
                        f'sns_id : {sns_id} | name : {name} | profile_image : {profile_image}')

            token_info = _create_token(user.user_id)
            _delete_refresh_token()

            session.commit()

            return token_info

    @staticmethod
    def renew_token(refresh_token: str) -> dict:
        jwt_factory = JWTFactory()
        token_info = jwt_factory.renew_token(refresh_token)
        _delete_refresh_token()

        return token_info
