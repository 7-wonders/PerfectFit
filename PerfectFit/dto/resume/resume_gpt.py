from dataclasses import dataclass, field
from typing import List, Optional

from domain.models import Job
from domain.models import ProjectExperience, Resume
from domain.models import WorkExperience
from dto.job.job import JobDto


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

    class Response:
        @dataclass
        class Section:
            title: str
            content: str

        class FullResume:
            @dataclass
            class Answer:
                sections: List['ResumeGPT.Response.Section']

            @dataclass
            class Resume:
                keywords: List[str]
                job: 'JobDto.Response.JobInfo'
                level: str
                pros: str
                cons: str
                sections: List['ResumeGPT.Response.Section']
                directional: Optional[str] = field(default=None)
                chapter: Optional[str] = field(default=None)
