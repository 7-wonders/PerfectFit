import os
import uuid

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType

from utils.oauth.oauth_handler import OAuthHandler


class KakaoOAuthHandler(OAuthHandler):
    def __init__(self):
        self.login_error_type = ExceptionType.KAKAO_LOGIN_ERROR
        self.client_id = os.environ.get('KAKAO_CLIENT_ID')
        self.client_secret_key = os.environ.get('KAKAO_SECRET_KEY')
        self.redirect_uri = os.environ.get('KAKAO_REDIRECT_URI')
        self.token_base_url = 'https://kauth.kakao.com/oauth/token'
        self.user_base_url = 'https://kapi.kakao.com/v2/user/me'

        if not self._check_environment():
            raise CustomException(ExceptionType.KAKAO_ENVIRONMENT_ERROR)

    def _check_environment(self) -> bool:
        return all([self.client_id, self.client_secret_key, self.redirect_uri])

    def get_login_url(self) -> str:
        return f'https://kauth.kakao.com/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&state={uuid.uuid4()}'

    def get_token_url(self) -> str:
        return self.token_base_url

    def get_user_info_url(self) -> str:
        return self.user_base_url

    def get_client_id(self) -> str:
        return self.client_id

    def get_client_secret(self) -> str:
        return self.client_secret_key

    def get_redirect_uri(self) -> str:
        return self.redirect_uri
