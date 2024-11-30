from dataclasses import dataclass

from dto.resume_section.resume_section import ResumeSectionDto


class MainDto:
    class Response:
        @dataclass
        class Population:
            resumeId: int
            title: str
            level: str
            viewCount: int
            likeCount: int
            occupationName: str
            jobName: str
            username: str
            section: "ResumeSectionDto.Response.Section"
            interviews: list["InterviewDto.Response.Interview"]
