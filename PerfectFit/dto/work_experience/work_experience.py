from dataclasses import dataclass
from datetime import date


class WorkExperienceDTO:
    class Response:
        @dataclass
        class WorkExperience:
            workExperienceId: int
            fromDate: date
            toDate: date
            companyName: str
            position: str
            reason: str
            responsibility: str
