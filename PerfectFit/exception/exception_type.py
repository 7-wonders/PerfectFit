from enum import Enum


class ExceptionType(Enum):
    NOT_FOUND_USER = ("404", "N40410", "사용자를 찾을 수 없습니다.")
    NOT_FOUND_JOB = ("404", "N40420", "직업을 찾을 수 없습니다.")
    NOT_FOUND_OCCUPATION = ("404", "N40421", "직군을 찾을 수 없습니다.")
    INTERNAL_SERVER_ERROR = ("500", "I500", "서버 내부에서 오류가 발생하였습니다.")

    @property
    def status_code(self):
        return self.value[0]

    @property
    def error_code(self):
        return self.value[1]

    @property
    def message(self):
        return self.value[2]
