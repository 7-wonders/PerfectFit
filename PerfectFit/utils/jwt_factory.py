import os
from uuid import uuid4

import jwt

from datetime import datetime, timedelta, timezone

from config.config_redis import Redis
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger

logger = Logger("jwt_factory")


class JWTFactory:
    """ JWT 토큰을 생성하고, 검증하는 클래스 """
    _key_refresh_token = "refreshtoken:"
    _conf_names = [
        "ACCESS_TOKEN_PRIVATE_KEY_NAME",
        "ACCESS_TOKEN_PUBLIC_KEY_NAME",
        "REFRESH_TOKEN_PRIVATE_KEY_NAME",
        "REFRESH_TOKEN_PUBLIC_KEY_NAME",
    ]
    _instance = None
    _access_private_key = None
    _access_public_key = None
    _refresh_private_key = None
    _refresh_public_key = None
    _algorithm = None
    _issuer = None
    _redis = None

    @classmethod
    def initialize_pool(cls):
        if cls._instance is None:
            cls._validate_environment_variables()

            cls._access_private_key = cls._load_key(os.getenv(cls._conf_names[0]))
            cls._access_public_key = cls._load_key(os.getenv(cls._conf_names[1]))
            cls._refresh_private_key = cls._load_key(os.getenv(cls._conf_names[2]))
            cls._refresh_public_key = cls._load_key(os.getenv(cls._conf_names[3]))

            cls._algorithm = os.getenv("JWT_ALGORITHM") or "RS256"
            cls._issuer = os.getenv("JWT_ISSUER") or "localhost"

            cls._initialize_redis()
            cls._instance = JWTFactory()

    @classmethod
    def _validate_environment_variables(cls):
        missing_vars = [var for var in cls._conf_names if not os.getenv(var)]
        if missing_vars:
            logger.error(f"Missing JWT configuration: {', '.join(missing_vars)}")
            raise CustomException(ExceptionType.JWT_CONF_ERROR)

    @classmethod
    def _load_key(cls, key_name):
        try:
            with open(key_name, "r") as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Error loading key file {key_name}: {str(e)}")
            raise CustomException(ExceptionType.JWT_CONF_ERROR)

    @classmethod
    def _initialize_redis(cls):
        cls._redis = Redis()

    def create_token(self, user_id: int) -> dict:
        """
            JWT 토큰을 생성하는 메소드
            AccessToken과 RefreshToken을 생성합니다.
         """
        uuid = str(uuid4())
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
            self._access_private_key,
            algorithm=self._algorithm,
        )

        refresh_token = jwt.encode({
            'token_id': uuid,
            'user_id': user_id,
            'exp': refresh_token_expiration,
            'iss': self._issuer,
        },
            self._refresh_private_key,
            algorithm=self._algorithm,
        )

        self._redis.save_with_unix_timestamp(
            f"{self._key_refresh_token}{uuid}",
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
        try:
            decoded = jwt.decode(access_token, self._access_public_key, algorithms=[self._algorithm], issuer=self._issuer)
            user_id = decoded.get('user_id')

            if user_id is None:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            return int(user_id)
        except jwt.ExpiredSignatureError:
            raise CustomException(ExceptionType.EXPIRED_TOKEN)
        except jwt.InvalidTokenError:
            raise CustomException(ExceptionType.INVALID_TOKEN)

    def _verify_refresh_token(self, refresh_token: str) -> int:
        """
            RefreshToken을 검증하는 메소드
            성공 여부를 반환합니다.
        """
        token_id = None

        try:
            decoded_refresh_token = jwt.decode(refresh_token, self._refresh_public_key, algorithms=[self._algorithm],
                                               issuer=self._issuer, options={'verify_exp': False})
            token_id = decoded_refresh_token.get('token_id')

            if token_id is None:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            redis_refresh_token = self._redis.get(f'{self._key_refresh_token}{token_id}')
            if redis_refresh_token is None or redis_refresh_token != refresh_token:
                raise CustomException(ExceptionType.INVALID_TOKEN)

            # RT의 만료 시간이 지났다면, 삭제 후 에러 반환
            if datetime.utcnow() > datetime.fromtimestamp(decoded_refresh_token.get('exp')):
                self._redis.delete(f"{self._key_refresh_token}{token_id}")
                raise CustomException(ExceptionType.INVALID_TOKEN)

            user_id = decoded_refresh_token.get('user_id')

            if user_id is None:
                self._redis.delete(f"{self._key_refresh_token}{token_id}")
                raise CustomException(ExceptionType.INVALID_TOKEN)

            return int(user_id)
        except jwt.ExpiredSignatureError:
            if token_id:
                self._redis.delete(f"{self._key_refresh_token}{token_id}")
            raise CustomException(ExceptionType.EXPIRED_TOKEN)
        except jwt.InvalidTokenError:
            if token_id:
                self._redis.delete(f"{self._key_refresh_token}{token_id}")
            raise CustomException(ExceptionType.INVALID_TOKEN)

    def delete_refresh_token(self, refresh_token: str):
        decoded_refresh_token = jwt.decode(refresh_token, self._refresh_public_key, algorithms=[self._algorithm],
                                           issuer=self._issuer, options={'verify_exp': False})
        token_id = decoded_refresh_token.get('token_id')

        if token_id is None:
            raise CustomException(ExceptionType.INVALID_TOKEN)

        self._redis.delete(f"{self._key_refresh_token}{token_id}")

    def renew_token(self, refresh_token: str) -> dict:
        """
            AccessToken을 갱신하는 메소드 (RTR 기법)
            갱신된 AccessToken과 RefreshToken을 반환합니다.
        """
        try:
            user_id = self._verify_refresh_token(refresh_token)
            return self.create_token(user_id)
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid Token {e}")
            raise CustomException(ExceptionType.INVALID_TOKEN)
