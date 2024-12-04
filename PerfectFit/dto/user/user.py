from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dto.project_experience.project_experience import PexDTO
    from dto.resume.resume import ResumeDto
    from dto.work_experience.work_experience import WorkExperienceDTO


class UserDto:
    class Request:
        @dataclass
        class CreateRequirementsRequest:
            keywords: List[str] = field(default_factory=list)
            job_id: Optional[int] = None
            level: Optional[str] = None
            pros: Optional[str] = None
            cons: Optional[str] = None
            prompt: Optional[str] = ""
            title: List[str] = field(default_factory=list)

            def __init__(self, **data):
                """
                지시된 방식으로 데이터 초기화 (**data 사용)
                """
                self.keywords = data.get("keywords", [])
                self.job_id = data.get("jobId")
                self.level = data.get("level")
                self.pros = data.get("pros")
                self.cons = data.get("cons")
                self.prompt = data.get("prompt", "")
                self.title = data.get("title", [])

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

        @dataclass
        class UserDetail:
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

        @dataclass
        class DetailUser:
            user: 'UserDto.Response.UserDetail'
            work_experiences: List['WorkExperienceDTO.Response.WorkExperience']
            project_experiences: List['PexDTO.Response.ProjectExperience']
            resumes: List['ResumeDto.Response.MyResume'] = field(default=None)
