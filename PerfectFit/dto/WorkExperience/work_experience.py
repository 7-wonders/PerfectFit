from dataclasses import dataclass
from datetime import date

class WorkExperienceDTO:
    class Response:
        @dataclass
        class WorkExperience:
            work_experience_id: int
            from_date: date
            to_date: date
            company_name: str
            position: str
            responsibility: str