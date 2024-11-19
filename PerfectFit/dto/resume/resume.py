from dataclasses import dataclass, field
from typing import List, Optional


class ResumeDto:
    class Request:
        @dataclass
        class CreateFullResume:
            keywords: List[str]
            job_id: int
            level: str
            pros: str
            cons: str
            directional: Optional[str] = field(default=None)
            chapter: Optional[str] = field(default=None)

        @dataclass
        class CreatePartialResume:
            keywords: List[str]
            job_id: int
            level: str
            pros: str
            cons: str
            directional: Optional[str]
