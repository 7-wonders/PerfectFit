from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

from domain.models import ProjectExperience
from domain.models import WorkExperience


if TYPE_CHECKING:
    from dto.resume.resume import ResumeDto


class ResumeGPT:
    class Request:
        class FullResume:
            @dataclass
            class Create:
                keywords: List[str]
                job_name: str
                level: str
                pros: str
                cons: str
                directional: Optional[str] = field(default=None)
                chapter: Optional[str] = field(default=None)
                work_experiences: Optional[List["WorkExperience"]] = field(default=None)
                project_experiences: Optional[List["ProjectExperience"]] = field(default=None)

        class PartialResume:
            @dataclass
            class Create:
                keywords: List[str]
                job_name: str
                level: str
                pros: str
                cons: str
                chapter_title: str
                directional: Optional[str] = field(default=None)
                work_experiences: Optional[List["WorkExperience"]] = field(default=None)
                project_experiences: Optional[List["ProjectExperience"]] = field(default=None)

    class Response:
        @dataclass
        class Answer:
            sections: List['ResumeDto.Section']

        class FullResume:
            @dataclass
            class Resume:
                keywords: List[str]
                job_id: int
                level: str
                pros: str
                cons: str
                sections: List['ResumeDto.Section']
                directional: Optional[str] = field(default=None)
                chapter: Optional[str] = field(default=None)
