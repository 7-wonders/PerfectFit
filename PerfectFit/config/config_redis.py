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

        missing_vars = [var_name for var_name, var_value in
                        zip(["REDIS_HOST", "REDIS_PORT", "REDIS_USERNAME", "REDIS_PASSWORD"],
                            [self._hostname, self._port, self._username, self._password]) if var_value is None]

        if missing_vars:
            logger.error(f"Missing Redis configuration: {', '.join(missing_vars)}")
            raise CustomException(ExceptionType.REDIS_CONF_ERROR)

        self._connection_pool = redis.ConnectionPool(
            host=self._hostname,
            port=self._port,
            username=self._username,
            password=self._password,
            max_connections=100,
            socket_timeout=5,
            socket_connect_timeout=5,
            decode_responses=True
        )
        self._redis_instance = redis.Redis(connection_pool=self._connection_pool)

    def get_instance(self):
        """
            Redis 객체를 반환하는 메소드

            최대 연결 수: 100
            소켓 타임아웃: 5초
            소켓 연결 타임아웃: 5초
            반환 타입: 문자열 (UTF-8)
        """
        return self._redis_instance

    def save_with_unix_timestamp(self, key: str, value: str, unix_time: int):
        """
        Redis에 데이터를 저장합니다.
        :param unix_time: 만료 시간 설정 (Unix Timestamp)
        :param key: 식별자
        :param value: 저장할 값
        :return: None
        """
        try:
            self.get_instance().set(key, value)
            # 만료 시간 설정 (Unix Timestamp)
            self.get_instance().expireat(key, unix_time)
        except redis.RedisError as e:
            logger.error(f"Redis 저장 중 '{key}' key 값을 가진 데이터에서 문제가 발생하였습니다. {e}")
            raise CustomException(ExceptionType.REDIS_DATA_ERROR)

    def get(self, key: str):
        """
        Redis에서 데이터를 조회합니다.
        :param key: 식별자
        :return: 조회된 값
        """
        try:
            return self.get_instance().get(key)
        except redis.RedisError as e:
            logger.error(f"Redis 데이터 조회 중 '{key}' key 값을 가진 데이터에서 문제가 발생하였습니다. {e}")
            raise CustomException(ExceptionType.REDIS_DATA_ERROR)

    def delete(self, key: str):
        """
        Redis에서 데이터를 삭제합니다.
        :param key: 식별자
        :return: None
        """
        try:
            self.get_instance().delete(key)
        except redis.RedisError as e:
            logger.error(f"Redis 데이터 삭제 중 '{key}' key 값을 가진 데이터에서 문제가 발생하였습니다. {e}")
            raise CustomException(ExceptionType.REDIS_DATA_ERROR)
