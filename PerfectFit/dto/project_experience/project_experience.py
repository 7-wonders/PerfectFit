from dataclasses import dataclass
from typing import List
from datetime import date


class PexDTO:  # ProjectExperienceDTO를 줄여서 작성하였습니다.
    class Response:
        @dataclass
        class ProjectExperienceContent:
            project_experience_task_id: int
            content: str

        @dataclass
        class ProjectExperience:
            projectExperienceId: int
            projectName: str
            fromDate: date
            toDate: date
            contents: List['PexDTO.Response.ProjectExperienceContent']
