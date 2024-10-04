from dataclasses import dataclass

## 값을 가공하는 용도. 리스폰스 맞춰주는 용도.
class UserDto:
    class Response:
        @dataclass
        class IntroUser:
            id: int
            name: str

        @dataclass
        class Users:
            users: list['UserDto.Response.IntroUser']
            pages: int
