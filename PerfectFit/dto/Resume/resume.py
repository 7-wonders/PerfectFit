from dataclasses import dataclass
from datetime import date, datetime

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