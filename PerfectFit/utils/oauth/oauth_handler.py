import requests

from abc import ABC, abstractmethod
from typing import Tuple, Mapping

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger

logger = Logger('oauth_handler')


class OAuthHandler(ABC):
    """OAuthHandler는 OAuth 인증 과정을 추상화한 클래스입니다.
    각 서비스별로 필요한 URL과 클라이언트 정보를 제공하는 메소드를 오버라이딩하여 사용합니다.
    """

    login_error_type: ExceptionType

    @abstractmethod
    def get_login_url(self) -> str:
        """로그인 페이지로 리디렉션할 URL을 반환합니다."""
        pass

    @abstractmethod
    def get_token_url(self) -> str:
        """OAuth 토큰을 요청할 URL을 반환합니다."""
        pass

    @abstractmethod
    def get_user_info_url(self) -> str:
        """사용자 정보를 요청할 URL을 반환합니다."""
        pass

    @abstractmethod
    def get_client_id(self) -> str:
        """클라이언트 ID를 반환합니다."""
        pass

    @abstractmethod
    def get_client_secret(self) -> str:
        """클라이언트 비밀 키를 반환합니다."""
        pass

    @abstractmethod
    def get_redirect_uri(self) -> str:
        """리디렉션 URI를 반환합니다."""
        pass

    @abstractmethod
    def _check_environment(self) -> bool:
        """환경 변수가 올바르게 설정되어 있는지 확인합니다."""
        pass

    def _check_access_token(access_token: str, token_type: str):
        """액세스 토큰과 토큰 유형이 올바르게 설정되어 있는지 확인합니다."""
        if not access_token or not token_type:
            logger.error(f'Token Request Error\n'
                         f'access_token : {access_token} | token_type : {token_type}')
            return False

        return True

    def get_access_token(self, code: str, **kwargs) -> Tuple[str, str]:
        """주어진 코드를 사용하여 액세스 토큰과 토큰 유형을 요청합니다."""
        token_params = {
            'code': code,
            'client_id': self.get_client_id(),
            'client_secret': self.get_client_secret(),
            'redirect_uri': self.get_redirect_uri(),
            'grant_type': 'authorization_code',
            **kwargs
        }
        response = requests.post(self.get_token_url(), data=token_params)

        if response.status_code != 200:
            logger.error(f'Token Request Error : status_code : {response.status_code}')
            raise CustomException(self.login_error_type)

        response_json = response.json()

        # 토큰과 토큰 유형 반환
        return response_json.get('access_token'), response_json.get('token_type')

    def get_user_info(self, token_type: str, access_token: str) -> Mapping:
        """액세스 토큰을 사용하여 사용자 정보를 요청합니다."""
        headers = {'Authorization': f'{token_type} {access_token}'}
        response = requests.get(self.get_user_info_url(), headers=headers)

        if response.status_code != 200:
            logger.error(f'User Request Error : status_code : {response.status_code}')
            raise CustomException(self.login_error_type)

        return response.json()
