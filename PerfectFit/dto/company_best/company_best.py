from dataclasses import dataclass
from pydantic import BaseModel
from typing import List

class CompanyBestDto:
    class Response:
        @dataclass
        class CompanyBest:
            companyBestId: int
            content: str
