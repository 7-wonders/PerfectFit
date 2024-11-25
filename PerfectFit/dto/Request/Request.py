from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class RequestDTO:
    @dataclass
    class CreateRequirementsRequest:
        keywords: List[str] = field(default_factory=list)
        job_id: Optional[int] = None
        level: Optional[str] = None
        pros: Optional[str] = None
        cons: Optional[str] = None
        prompt: Optional[str] = ""
        title: List[str] = field(default_factory=list)

        def __init__(self, **data):
            """
            지시된 방식으로 데이터 초기화 (**data 사용)
            """
            self.keywords = data.get("keywords", [])
            self.job_id = data.get("jobId")
            self.level = data.get("level")
            self.pros = data.get("pros")
            self.cons = data.get("cons")
            self.prompt = data.get("prompt", "")
            self.title = data.get("title", [])