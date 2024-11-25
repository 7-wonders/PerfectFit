from dataclasses import dataclass
from typing import List, Optional

class DetailedUserDTO:
    class Response:
        @dataclass
        class DetailedUser:
            user_id: int
            username: str
            age: int
            major: str
            university: str
            university_status: str
            grade: float
            address: str
            detail_address: str
            email: str
            phone_number: str
            profile_path: str
            work_experiences: List['PexDTO.Response.WorkExperience']
            project_experiences: List['PexDTO.Response.ProjectExperience']
            resumes: List['PexDTO.Response.Resume']