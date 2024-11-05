import os
import redis

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger

logger = Logger("redis")


class Redis:
    """
        Redis 객체를 생성하는 클래스
    """
    def __init__(self):
        self._hostname = os.getenv("REDIS_HOST")
        self._port = os.getenv("REDIS_PORT")
        self._username = os.getenv("REDIS_USERNAME")
        self._password = os.getenv("REDIS_PASSWORD")

        if not all([self._hostname, self._port, self._username, self._password]):
            logger.error("Redis 설정 중 문제가 발생하였습니다.")
            raise CustomException(ExceptionType.REDIS_CONF_ERROR)

    def _get_instance(self):
        """
            Redis 객체를 반환하는 메소드

            최대 연결 수: 100
            소켓 타임아웃: 5초
            소켓 연결 타임아웃: 5초
            반환 타입: 문자열 (UTF-8)
        """
        try:
            connection_pool = redis.ConnectionPool(
                host=self._hostname,
                port=self._port,
                username=self._username,
                password=self._password,
                max_connections=100,
                socket_timeout=5,
                socket_connect_timeout=5,
                decode_responses=True
            )
            return redis.Redis(connection_pool=connection_pool)
        except Exception as e:
            logger.error(f"Redis 객체 생성 중 문제가 발생하였습니다. {e}")
            raise CustomException(ExceptionType.REDIS_CONF_ERROR)

    def save(self, key: str, value: str, expire_time: int):
        """
        Redis에 데이터를 저장합니다.
        :param expire_time: 만료 시간 설정 (초 단위: 3600 = 1시간)
        :param key: 식별자
        :param value: 저장할 값
        :return: None
        """
        try:
            self._get_instance().set(key, value)
            # 만료 시간 설정 (Unix Timestamp)
            self._get_instance().expireat(key, expire_time)
        except Exception as e:
            logger.error(f"Redis 데이터 저장 중 문제가 발생하였습니다. {e}")
            raise CustomException(ExceptionType.REDIS_DATA_ERROR)

    def get(self, key: str):
        """
        Redis에서 데이터를 조회합니다.
        :param key: 식별자
        :return: 조회된 값
        """
        try:
            return self._get_instance().get(key)
        except Exception as e:
            logger.error(f"Redis 데이터 조회 중 문제가 발생하였습니다. {e}")
            raise CustomException(ExceptionType.REDIS_DATA_ERROR)

    def delete(self, key: str):
        """
        Redis에서 데이터를 삭제합니다.
        :param key: 식별자
        :return: None
        """
        try:
            self._get_instance().delete(key)
        except Exception as e:
            logger.error(f"Redis 데이터 삭제 중 문제가 발생하였습니다. {e}")
            raise CustomException(ExceptionType.REDIS_DATA_ERROR)
