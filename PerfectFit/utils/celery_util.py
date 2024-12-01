from typing import Optional

from config.config_mysql import get_session
from dotenv import load_dotenv
import redis, os

load_dotenv()

hostname = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")
password = os.getenv("REDIS_PASSWORD")

# Redis 클라이언트 연결
redis_client = redis.StrictRedis(host=hostname, port=port, db=0, password=password, decode_responses=True)

TASK_KEY_PREFIX = "task:"  # 작업을 Redis에서 찾을 때 사용할 키 접두어

def create_task(user_id: int, question_id: int, status: str) -> str:
    task_id = generate_unique_task_id()
    task_data = {
        'user_id': user_id,
        'question_id': question_id,
        'status': status
    }

    # Redis에 작업 정보 저장 (Hash 자료형 사용)
    redis_client.hmset(TASK_KEY_PREFIX + task_id, task_data)
    return task_id
def check_task_status(user_id: int, question_id: int) -> Optional[dict]:
    # Redis에서 작업 상태 확인 (Hash 자료형에서 조회)
    keys = redis_client.keys(f"{TASK_KEY_PREFIX}*")
    for key in keys:
        task = redis_client.hgetall(key)
        if int(task.get('user_id')) == user_id and int(task.get('question_id')) == question_id:
            return task
    return None

def update_task_status(task_id: str, status: str):
    # Redis에서 작업 상태 업데이트 (Hash 자료형에서 필드 값 수정)
    redis_client.hset(TASK_KEY_PREFIX + task_id, 'status', status)


import uuid

def generate_unique_task_id() -> str:
    """
    Generates a unique task ID using UUID.
    """
    return str(uuid.uuid4())