import os
import uuid
import jwt

from datetime import datetime, timedelta, timezone

from config.config_redis import Redis
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType


class JWTFactory:
    """ JWT 토큰을 생성하고, 검증하는 클래스 """
    _redis = Redis()
    _key_refresh_token = "refreshtoken:"

    def __init__(self):
        self._access_secret_key = os.getenv("ACCESS_TOKEN_SECRET_KEY")
        self._refresh_secret_key = os.getenv("REFRESH_TOKEN_SECRET_KEY")
        self._algorithm = os.getenv("JWT_ALGORITHM") or "HS256"
        self._issuer = os.getenv("JWT_ISSUER") or "localhost"

    def create_token(self, user_id: int) -> dict:
        """
            JWT 토큰을 생성하는 메소드
            AccessToken과 RefreshToken을 생성합니다.
         """
        access_token_exp = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_TIME", 3600))
        refresh_token_exp = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_TIME", 86400))

        # 만료 시간 설정
        access_token_expiration = datetime.now(timezone.utc) + timedelta(seconds=access_token_exp)
        refresh_token_expiration = datetime.now(timezone.utc) + timedelta(seconds=refresh_token_exp)

        access_token = jwt.encode({
            'user_id': user_id,
            'exp': access_token_expiration,
            'iss': self._issuer,
        },
            self._access_secret_key,
            algorithm=self._algorithm,
        )

        refresh_token = jwt.encode({
            'rand_key': str(uuid.uuid4()),
            'exp': refresh_token_expiration,
            'iss': self._issuer,
        },
            self._refresh_secret_key,
            algorithm=self._algorithm,
        )

        self._redis.save(
            f"{self._key_refresh_token}{user_id}",
            refresh_token,
            int(refresh_token_expiration.timestamp())
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_exp': int(access_token_expiration.timestamp()),
            'refresh_token_exp': int(refresh_token_expiration.timestamp())
        }

    def verify_access_token(self, access_token: str) -> int:
        """
            AccessToken을 검증하는 메소드
            user_id를 반환합니다.
        """
        secret_key = self._access_secret_key

        try:
            decoded = jwt.decode(access_token, secret_key, algorithm=self._algorithm, issuer=self._issuer)
            user_id = decoded.get('user_id')

            if user_id is None:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            return user_id
        except jwt.ExpiredSignatureError:
            raise CustomException(ExceptionType.EXPIRED_TOKEN)
        except jwt.InvalidTokenError:
            raise CustomException(ExceptionType.INVALID_TOKEN)

    def verify_refresh_token(self, user_id: int, refresh_token: str) -> bool:
        """
            RefreshToken을 검증하는 메소드
            성공 여부를 반환합니다.
        """
        secret_key = self._refresh_secret_key

        try:
            decoded = jwt.decode(refresh_token, secret_key, algorithm=self._algorithm, issuer=self._issuer)
            rand_key = decoded.get('rand_key')

            if rand_key is None:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            saved_refresh_token = self._redis.get(f"{self._key_refresh_token}{user_id}")
            if saved_refresh_token is None or saved_refresh_token != refresh_token:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            return True
        except jwt.ExpiredSignatureError:
            self._redis.delete(f"{self._key_refresh_token}{user_id}")
            raise CustomException(ExceptionType.EXPIRED_TOKEN)
        except jwt.InvalidTokenError:
            self._redis.delete(f"{self._key_refresh_token}{user_id}")
            raise CustomException(ExceptionType.INVALID_TOKEN)

    def renew_access_token(self, user_id: int, access_token: str, refresh_token: str) -> dict:
        """
            AccessToken을 갱신하는 메소드 (RTR 기법)
            갱신된 AccessToken을 반환합니다.
        """
        try:
            decoded_access_token = jwt.decode(access_token, self._access_secret_key, algorithm=self._algorithm,
                                               issuer=self._issuer, options={'verify_exp': False})
            decoded_refresh_token = jwt.decode(refresh_token, self._refresh_secret_key, algorithm=self._algorithm,
                                                  issuer=self._issuer, options={'verify_exp': False})

            if decoded_access_token.get('user_id') != user_id or decoded_refresh_token.get('rand_key') is None:
                self._redis.delete(f"{self._key_refresh_token}{user_id}")
                raise CustomException(ExceptionType.INVALID_TOKEN)

            # AT와 RT의 만료시간이 지나지 않았다면
            if datetime.utcnow() <= datetime.fromtimestamp(decoded_access_token.get('exp'))\
                    and datetime.utcnow() <= datetime.fromtimestamp(decoded_refresh_token.get('exp')):
                self._redis.delete(f"{self._key_refresh_token}{user_id}")
                raise CustomException(ExceptionType.INVALID_TOKEN)

            return self.create_token(user_id)
        except jwt.InvalidTokenError:
            raise CustomException(ExceptionType.INVALID_TOKEN)
