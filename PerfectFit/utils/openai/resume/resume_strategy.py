from abc import ABC
from dataclasses import dataclass
from typing import List, Optional

from utils.openai.chat_gpt import ChatGPT


@dataclass
class CreateResume:
    keywords: List[str]
    job_name: str
    level: int
    pros: str
    cons: str
    directional: Optional[str]
    chapter: Optional[str]


@dataclass
class Resume:

    @dataclass
    class Section:
        title: str
        content: str

    sections: List[Section]


class ResumeStrategy(ChatGPT, ABC):
    """
    자기소개서 작성의 전략 패턴을 위한 인터페이스입니다.
    각 전략 클래스는 이 인터페이스를 구현해야 합니다.
    """

    @property
    def function_description(self) -> List[any]:
        return [{
            'name': 'get_resume',
            'description': '사용자가 제공한 정보를 바탕으로 자기소개서를 작성합니다.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'sections': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'title': {
                                    'type': 'string',
                                    'description': '자기소개서의 단락 제목입니다.'
                                },
                                'content': {
                                    'type': 'string',
                                    'description': '자기소개서의 단락 내용입니다.'
                                }
                            }
                        }
                    }
                },
                'required': ['sections', 'title', 'content']
            }
        }]
