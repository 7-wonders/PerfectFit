from dataclasses import dataclass, field
from typing import Optional

from dto.resume_section.resume_section import ResumeSectionDto
from dto.validation_class import FormModel


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
