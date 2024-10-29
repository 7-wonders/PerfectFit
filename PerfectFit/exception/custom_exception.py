from flask import jsonify

from exception.exception_type import ExceptionType


class CustomException(Exception):
    def __init__(self, exception_type: ExceptionType):
        self.exception = exception_type

    def __to_json__(self):
        return jsonify({
            "status_code": self.exception.status_code,
            "error_code": self.exception.error_code,
            "message": self.exception.message,
        })

    def __str__(self):
        return self.exception.message
