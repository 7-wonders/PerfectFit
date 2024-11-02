import os
from typing import Mapping

import requests

from constants.sns_kind import SnsKind
from database.config import get_session
from domain.models import AppUser
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from utils.age import get_age
from utils.oauth.google_oauth_handler import GoogleOAuthHandler
from utils.oauth.kakao_oauth_handler import KakaoOAuthHandler
from utils.oauth.naver_oauth_handler import NaverOAuthHandler

logger = Logger('auth_service')


class AuthService:
    @staticmethod
    def google_login(code: str):
        access_token, token_type = GoogleOAuthHandler().get_access_token(code)
        user_response_json = GoogleOAuthHandler().get_user_info(token_type, access_token)

        sns_id = user_response_json.get('id')
        email = user_response_json.get('email')
        name = user_response_json.get('name')
        profile_image = user_response_json.get('picture')

        if not AuthService._check_enough_info(sns_id, name):
            logger.error(f'User Request Error\n'
                         f'sns_id : {sns_id} | email : {email} | name : {name}')
            raise CustomException(ExceptionType.GOOGLE_NOT_ENOUGH_INFO)

        already_user = get_session().query(AppUser).filter(AppUser.sns_id == sns_id).first()
        if already_user:
            # JWT 발급
            return

        user = AppUser(sns_id=sns_id, sns_kind=SnsKind.GOOGLE.value, email=email, username=name,
                       profile_path=profile_image)
        get_session().add(user)
        get_session().commit()
        logger.info(f'Google Signup Success\n'
                    f'sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image}')

    @staticmethod
    def naver_login(code: str, state: str):
        access_token, token_type = NaverOAuthHandler().get_access_token(code, state=state)
        user_response_json = NaverOAuthHandler().get_user_info(token_type, access_token)

        sns_id = user_response_json.get('response').get('id')
        name = user_response_json.get('response').get('name')
        email = user_response_json.get('response').get('email')
        profile_image = user_response_json.get('response').get('profile_image')
        phone_number = str(user_response_json.get('response').get('mobile')).replace('-', '')

        if not AuthService._check_enough_info(sns_id, name):
            logger.error(f'User Request Error\n'
                         f'sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image} | phone_number : {phone_number}')
            raise CustomException(ExceptionType.NAVER_NOT_ENOUGH_INFO)

        already_user = get_session().query(AppUser).filter(AppUser.sns_id == sns_id).first()
        if already_user:
            # JWT 발급
            return

        # MM-DD 형식
        response_birthday = user_response_json.get('response').get('birthday')
        birth_year = user_response_json.get('response').get('birthyear')
        birth_month, birth_day = map(int, response_birthday.split('-'))
        age = get_age(int(birth_year), birth_month, birth_day)

        user = AppUser(sns_id=sns_id, sns_kind=SnsKind.NAVER.value, email=email, username=name,
                       profile_path=profile_image, phone_number=phone_number, age=age)
        get_session().add(user)
        get_session().commit()

        logger.info(f'Naver Signup Success\n'
                    f'sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image} | phone_number : {phone_number} | age : {age}')

    @staticmethod
    def kakao_login(code: str, state: str):
        access_token, token_type = KakaoOAuthHandler().get_access_token(code, state=state)
        user_response_json = KakaoOAuthHandler().get_user_info(token_type, access_token)

        sns_id = user_response_json.get('id')
        name = user_response_json.get('properties').get('nickname')
        profile_image = user_response_json.get('properties').get('profile_image')

        if not AuthService._check_enough_info(sns_id, name):
            logger.error(f'User Request Error\n'
                         f'sns_id : {sns_id} | name : {name} | profile_image : {profile_image}')
            raise CustomException(ExceptionType.KAKAO_NOT_ENOUGH_INFO)

        already_user = get_session().query(AppUser).filter(AppUser.sns_id == sns_id).first()
        if already_user:
            # JWT 발급
            return

        user = AppUser(sns_id=sns_id, sns_kind=SnsKind.KAKAO.value, username=name, profile_path=profile_image)
        get_session().add(user)
        get_session().commit()
        logger.info(f'Kakao Signup Success\n'
                    f'sns_id : {sns_id} | name : {name} | profile_image : {profile_image}')

    @staticmethod
    def _check_enough_info(sns_id: str, name: str) -> bool:
        if not sns_id or not name:
            return False

        return True
