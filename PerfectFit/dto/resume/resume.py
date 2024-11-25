from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

from dto.job.job import JobDto
from dto.keyword.keyword import KeywordDto
from dto.occupation.occupation import OccupationDto
from dto.resume_section.resume_section import ResumeSectionDto
from dto.user.user import UserDto
from dto.validation_class import FormModel


if TYPE_CHECKING:
    from dto.resume.resume_gpt import ResumeGPT


class ResumeDto:
    class Request:
        @dataclass
        class Create(FormModel):
            title: str
            keywords: list[str]
            job_id: int
            level: str
            pros: str
            cons: str
            is_shared: bool
            sections: list["ResumeSectionDto.Request.Create"]
            directional: Optional[str] = field(default=None)

            def __validation__(self):
                if not self.title.strip():
                    return "제목은 필수입니다."
                elif not self.keywords or len(self.keywords) < 1 or not any([keyword.strip() for keyword in self.keywords]):
                    return "키워드는 1개 이상이어야 합니다"
                elif not self.job_id or self.job_id < 1:
                    return "직업은 필수입니다."
                elif not self.level.strip():
                    return "신입, 경력만 선택할 수 있습니다."
                elif self.level not in ["신입", "경력"]:
                    return "신입, 경력만 선택할 수 있습니다."
                elif not self.pros.strip():
                    return "장점은 필수입니다."
                elif not self.cons.strip():
                    return "단점은 필수입니다."
                elif not self.is_shared:
                    return "공개 여부는 필수입니다."
                elif not self.sections or len(self.sections) < 1:
                    return "자기소개서 단락은 1개 이상이어야 합니다."

        @dataclass
        class Update(FormModel):
            title: str
            job_id: int
            level: str
            pros: str
            cons: str
            keywords: list["KeywordDto.Request.Update"]
            sections: list["ResumeSectionDto.Request.Update"]
            is_shared: bool = field(default=False)
            directional: Optional[str] = field(default=None)

            def __validation__(self):
                if not self.title.strip():
                    return "제목은 필수입니다."
                if not self.keywords or len(self.keywords) < 1 or not all([keyword.content.strip() for keyword in self.keywords]):
                    return "키워드는 1개 이상 또는 모두 공백이 아니어야 합니다."
                elif not self.job_id or self.job_id < 1:
                    return "직업은 필수입니다."
                elif not self.level.strip():
                    return "신입, 경력만 선택할 수 있습니다."
                elif self.level not in ["신입", "경력"]:
                    return "신입, 경력만 선택할 수 있습니다."
                elif not self.pros.strip():
                    return "장점은 필수입니다."
                elif not self.cons.strip():
                    return "단점은 필수입니다."
                elif (not self.sections or len(self.sections) < 1):
                    return "자기소개서 단락은 1개 이상 또는 모두 공백이 아니어야 합니다."

        @dataclass
        class CreateSectionContent:
            keywords: list[str]
            job_id: int
            level: str
            pros: str
            cons: str
            chapter_title: str
            directional: Optional[str] = field(default=None)


        @dataclass
        class CreateFullResume(FormModel):
            keywords: list[str]
            job_id: int
            level: str
            pros: str
            cons: str
            directional: Optional[str] = field(default=None)
            chapter: Optional[list[str]] = field(default=None)

            def __validation__(self):
                if not self.keywords or len(self.keywords) < 1 or not any([keyword.strip() for keyword in self.keywords]):
                    return "키워드는 1개 이상이어야 합니다"
                elif not self.job_id or self.job_id < 1:
                    return "직업은 필수입니다."
                elif self.level not in ["신입", "경력"]:
                    return "신입, 경력만 선택할 수 있습니다."
                elif not self.pros.strip():
                    return "장점은 필수입니다."
                elif not self.cons.strip():
                    return "단점은 필수입니다."

        @dataclass
        class CreatePartialResume:
            keywords: List[str]
            job_id: int
            level: str
            pros: str
            cons: str
            directional: Optional[str]

    class Response:
        @dataclass
        class ResumeForWrite:
            resume: "ResumeGPT.Response.FullResume.Resume" or None
            jobs: "JobDto.Response.Jobs" or None
            occupations: List["OccupationDto.Response.Occupation"]

        @dataclass
        class Resume:
            resumeId: int
            title: str
            jobName: str
            occupationName: str
            level: str
            likeCount: int
            viewCount: int
            createdTime: str
            user: "UserDto.Response.IntroUserWithProfile"
            section: list["ResumeSectionDto.Response.Section"]
            isLike: Optional[bool] = field(default=None)

        @dataclass
        class ResumeWithUpdate:
            resumeId: int
            title: str
            level: str
            pros: str
            cons: str
            keywords: list["KeywordDto.Response.Keyword"]
            directional: Optional[str]
            sections: list["ResumeSectionDto.Response.Section"]
            isPublic: bool

        @dataclass
        class ResumeForUpdate:
            resume: "ResumeDto.Response.ResumeWithUpdate"
            jobs: "JobDto.Response.Jobs"
            occupations: List["OccupationDto.Response.Occupation"]

        @dataclass
        class MyResumeInfo:
            resume_id: int
            title: str
            view_count: int
            like_count: int
            occupation: 'OccupationDto.Response.Occupation'
            job: str
            level: str
            created_time: datetime

        @dataclass
        class MyResume:
            user: 'UserDto.Response.IntroUserWithProfile'
            resumes: List['ResumeDto.Response.MyResumeInfo']
            total: int
