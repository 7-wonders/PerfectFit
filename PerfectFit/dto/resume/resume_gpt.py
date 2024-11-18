from dataclasses import dataclass, field
from typing import List, Optional

from domain.models import ProjectExperience
from domain.models import WorkExperience


class ResumeGPT:
    class Request:
        @dataclass
        class CreateResume:
            keywords: List[str]
            job_name: str
            level: int
            pros: str
            cons: str
            directional: Optional[str] = field(default=None)
            chapter: Optional[str] = field(default=None)
            work_experiences: Optional[List["WorkExperience"]] = field(default=None)
            project_experiences: Optional[List["ProjectExperience"]] = field(default=None)

    class Response:
        @dataclass
        class Resume:
            @dataclass
            class Section:
                title: str
                content: str

            sections: List[Section]
