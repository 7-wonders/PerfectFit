from enum import Enum


class ExceptionType(Enum):
    GOOGLE_NOT_ENOUGH_INFO = ("400", "B40010", "필수 정보가 부족합니다. e.g. id, email, name")
    NAVER_NOT_ENOUGH_INFO = ("400", "B40011", "필수 정보가 부족합니다. e.g. id, email, name")
    KAKAO_NOT_ENOUGH_INFO = ("400", "B40012", "필수 정보가 부족합니다. e.g. id, email, name")
    REQUIRED_KEYWORDS = ("400", "B40020", "중요 키워드는 필수입니다.")
    REQUIRED_JOB = ("400", "B40021", "직업는 필수입니다.")
    REQUIRED_LEVEL = ("400", "B40022", "경력은 필수입니다.")
    REQUIRED_PROS = ("400", "B40023", "장점은 필수입니다.")
    REQUIRED_CONS = ("400", "B40024", "단점은 필수입니다.")
    REQUIRED_CHAPTER_TITLE = ("400", "B40025", "단락의 제목은 필수입니다.")
    INVALID_JOB_ID = ("400", "B40030", "유효하지 않은 직업 ID입니다.")

    EXPIRED_TOKEN = ("401", "U40110", "토큰이 만료되었습니다.")
    INVALID_TOKEN = ("401", "U40111", "토큰이 유효하지 않습니다.")

    NOT_FOUND_USER = ("404", "N40410", "사용자를 찾을 수 없습니다.")

    NOT_FOUND_JOB = ("404", "N40420", "직업을 찾을 수 없습니다.")
    NOT_FOUND_OCCUPATION = ("404", "N40421", "직군을 찾을 수 없습니다.")
    NOT_FOUND_INTERVIEW = ("404", "N40430", "모의 면접을 찾을 수 없습니다.")
    NOT_FOUND_QUESTION = ("404", "N40431", "질문을 찾을 수 없습니다.")

    INTERNAL_SERVER_ERROR = ("500", "I500", "서버 내부에서 오류가 발생하였습니다.")
    GOOGLE_LOGIN_ERROR = ("500", "I50010", "구글 로그인에 문제가 발생하였습니다.")
    GOOGLE_ENVIRONMENT_ERROR = ("500", "I50011", "구글 환경 변수가 설정되지 않았습니다.")
    NAVER_LOGIN_ERROR = ("500", "I50012", "네이버 로그인에 문제가 발생하였습니다.")
    NAVER_ENVIRONMENT_ERROR = ("500", "I50013", "네이버 환경 변수가 설정되지 않았습니다.")
    KAKAO_LOGIN_ERROR = ("500", "I50014", "카카오 로그인에 문제가 발생하였습니다.")
    KAKAO_ENVIRONMENT_ERROR = ("500", "I50015", "카카오 환경 변수가 설정되지 않았습니다.")
    REDIS_CONF_ERROR = ("500", "I50020", "Redis 설정 중 문제가 발생하였습니다.")
    REDIS_DATA_ERROR = ("500", "I50021", "Redis 데이터 조작 중 오류가 발생하였습니다.")
    JWT_CONF_ERROR = ("500", "I50030", "JWT 설정 중 문제가 발생하였습니다.")
    GPT_CONF_ERROR = ("500", "I50040", "GPT 설정 중 문제가 발생하였습니다.")
    CELERY_ERROR = ("500", "I50050", "백그라운드 작업 중 문제가 발생하였습니다.")

    @property
    def status_code(self):
        return self.value[0]

    @property
    def error_code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]
