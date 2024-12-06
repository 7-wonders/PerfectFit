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

        @dataclass
        class Interview:
            interviewId: int
            title : str
            level : str
            viewCount: int
            likeCount: int
            occupationName : str
            jobName : str
            question: str
            answer: str

        @dataclass
        class MainPopulation:
            resumes: list["MainDto.Response.Population"]
            interviews: list["MainDto.Response.Interview"]


