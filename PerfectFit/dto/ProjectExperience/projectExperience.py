from dataclasses import dataclass
from typing import List, Optional
from datetime import date

class PexDTO: # ProjectExperienceDTO를 줄여서 작성하였습니다.
    class Response:
        @dataclass
        class WorkExperience:
            work_experience_id: int
            from_date: date
            to_date: date
            company_name: str
            position: str
            responsibility: str

        @dataclass
        class ProjectExperienceContent:
            project_experience_task_id: int
            content: str

        @dataclass
        class ProjectExperience:
            project_experience_id: int
            project_name: str
            from_date: date
            to_date: date
            contents: List['UserDto.Response.ProjectExperienceContent']

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
            work_experiences: List['UserDto.Response.WorkExperience']
            project_experiences: List['UserDto.Response.ProjectExperience']