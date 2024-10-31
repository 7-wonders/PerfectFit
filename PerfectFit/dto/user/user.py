from dataclasses import dataclass


class UserDto:
    class Response:
        @dataclass
        class IntroUser:
            user_id: int
            username: str

        @dataclass
        class Users:
            users: list['UserDto.Response.IntroUser']
            pages: int

