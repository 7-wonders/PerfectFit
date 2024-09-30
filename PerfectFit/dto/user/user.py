from dataclasses import dataclass


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
