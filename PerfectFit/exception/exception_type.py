from enum import Enum


class ExceptionType(Enum):
    GOOGLE_NOT_ENOUGH_INFO = ("400", "B40010", "구글 로그인 정보가 부족합니다. e.g. id, email, name")

    NOT_FOUND_USER = ("404", "N40410", "사용자를 찾을 수 없습니다.")

    INTERNAL_SERVER_ERROR = ("500", "I500", "서버 내부에서 오류가 발생하였습니다.")
    GOOGLE_LOGIN_ERROR = ("500", "I50010", "구글 로그인에 문제가 생겼습니다.")

    @property
    def status_code(self):
        return self.value[0]

    @property
    def error_code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]
