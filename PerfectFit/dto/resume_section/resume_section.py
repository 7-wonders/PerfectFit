from dataclasses import dataclass, field


@dataclass
class SectionPartialId:
    title: str
    content: str
    section_id: int = field(default=None)


class ResumeSectionDto:
    class Request:
        @dataclass
        class Create(SectionPartialId):
            pass

        @dataclass
        class Update(SectionPartialId):
            pass

    class Response:
        @dataclass
        class Section:
            title: str
            content: str
            sectionId: int = field(default=None)
