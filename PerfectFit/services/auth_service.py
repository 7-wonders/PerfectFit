import os

import requests

from constants.sns_kind import SnsKind
from database.config import get_session
from domain.models import AppUser
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger

logger = Logger("auth_service")


class AuthService:
    @staticmethod
    def google_login(code: str):
        token_base_url = "https://oauth2.googleapis.com/token"
        user_base_url = "https://www.googleapis.com/userinfo/v2/me"
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        client_secret_key = os.environ.get('GOOGLE_SECRET_KEY')
        redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')

        if not client_id or not client_secret_key or not redirect_uri:
            logger.info(f"Google Environment Error\n"
                        f"client_id : {client_id} | client_secret_key : {client_secret_key} | redirect_uri : {redirect_uri}")
            raise CustomException(ExceptionType.GOOGLE_LOGIN_ERROR)

        token_params = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret_key,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        }

        token_response = requests.post(token_base_url, data=token_params)
        token_response_json = token_response.json()

        if token_response.status_code != 200:
            logger.error(f"Token Request Error\n"
                         f"status_code : {token_response.status_code} | response : {token_response_json}")
            raise CustomException(ExceptionType.GOOGLE_LOGIN_ERROR)

        access_token = token_response_json.get('access_token')
        token_type = token_response_json.get('token_type')

        if not access_token or not token_type:
            logger.error(f"Token Request Error\n"
                         f"access_token : {access_token} | token_type : {token_type}")
            raise CustomException(ExceptionType.GOOGLE_LOGIN_ERROR)

        user_response = requests.get(user_base_url, headers={"Authorization": f"{token_type} {access_token}"})
        user_response_json = user_response.json()

        if user_response.status_code != 200:
            logger.error(f"User Request Error\n"
                         f"status_code : {user_response.status_code} | response : {user_response_json}")
            raise CustomException(ExceptionType.GOOGLE_LOGIN_ERROR)

        sns_id = user_response_json.get('id')
        email = user_response_json.get('email')
        name = user_response_json.get('name')
        profile_image = user_response_json.get('picture')

        if not sns_id or not name:
            logger.error(f"User Request Error\n"
                         f"sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image}")
            raise CustomException(ExceptionType.GOOGLE_NOT_ENOUGH_INFO)

        already_user = get_session().query(AppUser).filter(AppUser.sns_id == sns_id).first()
        if already_user:
            # JWT 발급
            return

        user = AppUser(sns_id=sns_id, sns_kind=SnsKind.GOOGLE.value, email=email, username=name, profile_path=profile_image)
        get_session().add(user)
        get_session().commit()
        logger.info(f"Google Login Success\n"
                    f"sns_id : {sns_id} | email : {email} | name : {name} | profile_image : {profile_image}")
