from dataclasses import dataclass
from datetime import datetime
from typing import List

class Interviews:

    class Response:
        @dataclass
        class Occupation:
            occupation_id: int
            occupation_name: str

        @dataclass
        class Interview:
            interview_id: int
            title: str
            is_public: bool
            view_count: int
            like_count: int
            occupation: 'interviews.Response.occupation'
            job: str
            level: str
            created_time: datetime

        @dataclass
        class UserInterviewsResponse:
            user_id: int
            username: str
            profile_path: str
            interviews: List['interviews.Response.Interview']
            total: int