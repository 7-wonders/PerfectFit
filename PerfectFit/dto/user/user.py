from dataclasses import dataclass
from typing import List, Optional
from datetime import date


class UserDto:
    class Response:
        @dataclass
        class IntroUser:
            user_id: int
            username: str

        @dataclass
        class IntroUserWithProfile:
            userId: int
            username: str
            profilePath: Optional[str]

        @dataclass
        class Users:
            users: List['UserDto.Response.IntroUser']
            pages: int
