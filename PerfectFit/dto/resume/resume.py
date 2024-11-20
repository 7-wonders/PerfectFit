from dataclasses import dataclass, field
from typing import List, Optional

from dto.validation_class import FormModel


class ResumeDto:
    @dataclass
    class Section:
        title: str
        content: str

    class Request:
        @dataclass
        class Create(FormModel):
            title: str
            keywords: list[str]
            job_id: int
            level: str
            pros: str
            cons: str
            is_shared: bool
            sections: list["ResumeDto.Section"]
            directional: Optional[str] = field(default=None)

            def __validation__(self):
                if not self.title.strip():
                    return "제목은 필수입니다."
                elif not self.keywords or len(self.keywords) < 1 or not any([keyword.strip() for keyword in self.keywords]):
                    return "키워드는 1개 이상이어야 합니다"
                elif not self.job_id or self.job_id < 1:
                    return "직업은 필수입니다."
                elif not self.level.strip():
                    return "신입, 경력만 선택할 수 있습니다."
                elif self.level not in ["신입", "경력"]:
                    return "신입, 경력만 선택할 수 있습니다."
                elif not self.pros.strip():
                    return "장점은 필수입니다."
                elif not self.cons.strip():
                    return "단점은 필수입니다."
                elif not self.is_shared:
                    return "공개 여부는 필수입니다."
                elif not self.sections or len(self.sections) < 1:
                    return "자기소개서 단락은 1개 이상이어야 합니다."

        @dataclass
        class CreateSectionContent:
            keywords: list[str]
            job_id: int
            level: str
            pros: str
            cons: str
            chapter_title: str
            directional: Optional[str] = field(default=None)


        @dataclass
        class CreateFullResume(FormModel):
            keywords: list[str]
            job_id: int
            level: str
            pros: str
            cons: str
            directional: Optional[str] = field(default=None)
            chapter: Optional[list[str]] = field(default=None)

            def __validation__(self):
                if not self.keywords or len(self.keywords) < 1 or not any([keyword.strip() for keyword in self.keywords]):
                    return "키워드는 1개 이상이어야 합니다"
                elif not self.job_id or self.job_id < 1:
                    return "직업은 필수입니다."
                elif self.level not in ["신입", "경력"]:
                    return "신입, 경력만 선택할 수 있습니다."
                elif not self.pros.strip():
                    return "장점은 필수입니다."
                elif not self.cons.strip():
                    return "단점은 필수입니다."

        @dataclass
        class CreatePartialResume:
            keywords: List[str]
            job_id: int
            level: str
            pros: str
            cons: str
            directional: Optional[str]
