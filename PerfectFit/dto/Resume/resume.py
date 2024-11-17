from dataclasses import dataclass
from datetime import datetime
from typing import List

class ResumeDTO:
    @dataclass
    class Resume:
        resume_id: int
        title: str
        view_count: int
        like_count: int
        occupation: 'PexDTO.Response.Occupation'
        job: str
        level: str
        created_time: datetime

    @dataclass
    class User:
        user_id: int
        username: str
        profile_path: str

    @dataclass
    class Response:
        user: 'ResumeDTO.User'
        resumes: List['ResumeDTO.Resume']
        total: int