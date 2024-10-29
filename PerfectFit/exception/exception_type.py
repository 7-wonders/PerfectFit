from enum import Enum


class ExceptionType(Enum):
    NOT_FOUND_USER = ("404", "N40410", "사용자를 찾을 수 없습니다.")
    INTERNAL_SERVER_ERROR = ("500", "I500", "서버 내부에서 오류가 발생하였습니다.")
    REQUIRED_SNS_KIND = ("400", "40010", "SNS KIND는 인자로 필요합니다.")
    REQUIRED_SNS_ID = ("400", "40011", "SNS ID는 인자로 필요합니다.")
    REQUIRED_NAME = ("400", "40012", "NAME은 인자로 필요합니다.")
    SNS_KIND_BAD_REQUEST = ("400", "40013", "SNS KIND의 값이 올바르지 않습니다.")
    NAME_BAD_REQUEST = ("400", "40014", "NAME의 값이 올바르지 않습니다.")

    @property
    def status_code(self):
        return self.value[0]

    @property
    def error_code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]
