from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from dto.job.job import JobDto
from dto.keyword.keyword import KeywordDto
from dto.occupation.occupation import OccupationDto
from dto.resume_section.resume_section import ResumeSectionDto
from dto.validation_class import FormModel

if TYPE_CHECKING:
    from dto.resume.resume import ResumeDto


class ResumeDraftDto:
    class Request:
        @dataclass
        class Create(FormModel):
            title: str
            keywords: list[str] = field(default=None)
            job_id: int = field(default=None)
            level: str = field(default=None)
            pros: str = field(default=None)
            cons: str = field(default=None)
            is_shared: bool = field(default=False)
            sections: list["ResumeSectionDto.Request.Create"] = field(default=None)
            directional: Optional[str] = field(default=None)

            def __validation__(self):
                if not self.title.strip():
                    return "제목은 필수입니다."

    class Response:
        @dataclass
        class Intro:
            draftId: int
            title: str
            createdTime: str

        @dataclass
        class DraftWithWrite:
            draftId: int
            title: str
            level: Optional[str] = field(default=None)
            pros: Optional[str] = field(default=None)
            cons: Optional[str] = field(default=None)
            keywords: Optional[list["KeywordDto.Response.Keyword"]] = field(default=None)
            directional: Optional[str] = field(default=None)
            sections: Optional[list["ResumeSectionDto.Response.Section"]] = field(default=None)
            isPublic: Optional[bool] = field(default=False)

        @dataclass
        class DraftForWrite:
            resume: "ResumeDraftDto.Response.DraftWithWrite"
            drafts: list["ResumeDraftDto.Response.Intro"]
            occupations: list["OccupationDto.Response.Occupation"]
            jobs: Optional[list["JobDto.Response.Jobs"]] = field(default=None)
