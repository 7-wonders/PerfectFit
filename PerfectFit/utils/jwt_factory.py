import os
import uuid
import jwt

from datetime import datetime, timedelta

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType


class JWTFactory:
    """ JWT 토큰을 생성하고, 검증하는 클래스 """

    def __init__(self):
        self._access_secret_key = os.getenv("ACCESS_TOKEN_SECRET_KEY")
        self._refresh_secret_key = os.getenv("REFRESH_TOKEN_SECRET_KEY")
        self._algorithm = os.getenv("JWT_ALGORITHM") or "HS256"
        self._issuer = os.getenv("JWT_ISSUER") or "localhost"

    def create_token(self, user_id: int) -> tuple[str, str]:
        """
            JWT 토큰을 생성하는 메소드
            AccessToken과 RefreshToken을 생성합니다.
         """
        access_token_exp = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_TIME"), 3600)
        refresh_token_exp = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_TIME"), 86400)

        access_token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=access_token_exp),
        },
            self._access_secret_key,
            algorithms=[self._algorithm],
            issuer=self._issuer,
        )

        refresh_token = jwt.encode({
            'rand_key': uuid.uuid4(),
            'exp': datetime.utcnow() + timedelta(seconds=refresh_token_exp),
        },
            self._refresh_secret_key,
            algorithms=[self._algorithm],
            issuer=self._issuer,
        )

        return access_token, refresh_token

    def verify_access_token(self, access_token: str) -> int:
        """
            AccessToken을 검증하는 메소드
            user_id를 반환합니다.
        """
        secret_key = self._access_secret_key

        try:
            decoded = jwt.decode(access_token, secret_key, algorithms=[self._algorithm], issuer=self._issuer)
            user_id = decoded.get('user_id')

            if user_id is None:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            return user_id
        except jwt.ExpiredSignatureError:
            raise CustomException(ExceptionType.EXPIRED_TOKEN)
        except jwt.InvalidTokenError:
            raise CustomException(ExceptionType.INVALID_TOKEN)

    def verify_refresh_token(self, refresh_token: str) -> bool:
        """
            RefreshToken을 검증하는 메소드
            성공 여부를 반환합니다.
        """
        secret_key = self._refresh_secret_key

        try:
            decoded = jwt.decode(refresh_token, secret_key, algorithms=[self._algorithm], issuer=self._issuer)
            rand_key = decoded.get('rand_key')

            if rand_key is None:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            return 'rand_key' in decoded
        except jwt.ExpiredSignatureError:
            raise CustomException(ExceptionType.EXPIRED_TOKEN)
        except jwt.InvalidTokenError:
            raise CustomException(ExceptionType.INVALID_TOKEN)
