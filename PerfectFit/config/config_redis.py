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
    _connection_pool = None

    @classmethod
    def initialize_pool(cls):
        if cls._connection_pool is None:
            hostname = os.getenv("REDIS_HOST")
            port = os.getenv("REDIS_PORT")
            username = os.getenv("REDIS_USERNAME")
            password = os.getenv("REDIS_PASSWORD")

            missing_vars = [var_name for var_name, var_value in
                            zip(["REDIS_HOST", "REDIS_PORT", "REDIS_USERNAME", "REDIS_PASSWORD"],
                                [hostname, port, username, password]) if var_value is None]

            if missing_vars:
                logger.error(f"Missing Redis configuration: {', '.join(missing_vars)}")
                raise CustomException(ExceptionType.REDIS_CONF_ERROR)

            cls._connection_pool = redis.ConnectionPool(
                host=hostname,
                port=port,
                username=username,
                password=password,
                max_connections=100,
                socket_timeout=5,
                socket_connect_timeout=5,
                decode_responses=True
            )

    def __init__(self):
        self._redis_instance = redis.Redis(connection_pool=self._connection_pool)

    def save_with_unix_timestamp(self, key: str, value: str, unix_time: int):
        """
        Redis에 데이터를 저장합니다.
        :param unix_time: 만료 시간 설정 (Unix Timestamp)
        :param key: 식별자
        :param value: 저장할 값
        :return: None
        """
        try:
            self._redis_instance.set(key, value)
            # 만료 시간 설정 (Unix Timestamp)
            self._redis_instance.expireat(key, unix_time)
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
            return self._redis_instance.get(key)
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
            self._redis_instance.delete(key)
        except redis.RedisError as e:
            logger.error(f"Redis 데이터 삭제 중 '{key}' key 값을 가진 데이터에서 문제가 발생하였습니다. {e}")
            raise CustomException(ExceptionType.REDIS_DATA_ERROR)

    def save(self, key: str, value: str):
        """Redis에 데이터를 저장하며 TTL 설정"""
        self._redis_instance.setex(key, 60, value)

    def save_verify(self, key: str, value: str):
        """Redis에 데이터를 저장하며 TTL 설정"""
        self._redis_instance.setex(key, 300, value)

    def get(self, key: str):
        """Redis에서 데이터를 가져오기"""
        return self._redis_instance.get(key)