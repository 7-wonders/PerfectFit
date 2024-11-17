from dataclasses import dataclass
from typing import List, Optional


class ResumeDto:
    class Request:
        @dataclass
        class CreateFullResume:
            keywords: List[str]
            job_id: int
            level: int
            pros: str
            cons: str
            directional: Optional[str]
            chapter: Optional[str]

        @dataclass
        class CreatePartialResume:
            keywords: List[str]
            job_id: int
            level: int
            pros: str
            cons: str
            directional: Optional[str]
