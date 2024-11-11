import os
import uuid

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType

from utils.oauth.oauth_handler import OAuthHandler


class NaverOAuthHandler(OAuthHandler):
    def __init__(self):
        self.login_error_type = ExceptionType.NAVER_LOGIN_ERROR
        self.client_id = os.environ.get('NAVER_CLIENT_ID')
        self.client_secret_key = os.environ.get('NAVER_SECRET_KEY')
        self.redirect_uri = os.environ.get('NAVER_REDIRECT_URI')
        self.token_base_url = 'https://nid.naver.com/oauth2.0/token'
        self.user_base_url = 'https://openapi.naver.com/v1/nid/me'

        if not self._check_environment():
            raise CustomException(ExceptionType.NAVER_ENVIRONMENT_ERROR)

    def _check_environment(self) -> bool:
        return all([self.client_id, self.client_secret_key, self.redirect_uri])

    def get_login_url(self) -> str:
        return f'https://nid.naver.com/oauth2.0/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&state={uuid.uuid4()}'

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
