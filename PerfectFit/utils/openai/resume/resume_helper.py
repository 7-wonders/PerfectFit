from typing import List

from openai.types.chat import ChatCompletion

from utils.openai.chat_gpt import ChatGPT
from utils.openai.resume.resume_strategy import ResumeStrategy


class ResumeHelper(ChatGPT):
    """
    자기소개서를 작성하는 데 도움을 주는 클래스입니다.
    ChatGPT를 활용하여 자기소개서를 작성하고, 전략 패턴을 사용하여 질문과 답변을 처리합니다.
    """

    def __init__(self, strategy: ResumeStrategy):
        super().__init__()
        self.strategy = strategy

    @property
    def function_description(self) -> List[any]:
        return self.strategy.function_description

    @property
    def system_content(self) -> str:
        return self.strategy.system_content

    @property
    def question(self) -> str:
        return self.strategy.question

    def parse_answer(self, completion: ChatCompletion) -> dict:
        return self.strategy.parse_answer(completion)
    