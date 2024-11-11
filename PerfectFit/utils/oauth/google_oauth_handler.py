import os

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType

from utils.oauth.oauth_handler import OAuthHandler


class GoogleOAuthHandler(OAuthHandler):
    def __init__(self):
        self.login_error_type = ExceptionType.GOOGLE_LOGIN_ERROR
        self.client_id = os.environ.get('GOOGLE_CLIENT_ID')
        self.client_secret_key = os.environ.get('GOOGLE_SECRET_KEY')
        self.redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
        self.token_base_url = 'https://accounts.google.com/o/oauth2/token'
        self.user_base_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        self.login_base_url = f'https://accounts.google.com/o/oauth2/v2/auth?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code&scope=email profile'

        if not self._check_environment():
            raise CustomException(ExceptionType.GOOGLE_ENVIRONMENT_ERROR)

    def _check_environment(self) -> bool:
        return all([self.client_id, self.client_secret_key, self.redirect_uri])

    def get_login_url(self) -> str:
        return self.login_base_url

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
