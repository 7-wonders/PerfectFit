import os

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletion

from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger

logger = Logger('chat_gpt')


class ChatGPT(ABC):
    """
    Chat GPT를 사용하기 위한 추상화된 클래스입니다.
    각 어시스턴트에 대해 필요한 정보를 명시하고, 사용은 구체화된 메소드를 사용합니다.
    """
    model_name = 'gpt-4o-mini'

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise CustomException(ExceptionType.GPT_CONF_ERROR)

        self.client = OpenAI(api_key=api_key)

    @property
    @abstractmethod
    def function_description(self) -> List[any]:
        """
        Chat GPT의 반환 값을 지정하는 변수입니다.

        해당 속성은 상속 받은 클래스에서 반드시 구현되어야 합니다.
        속성의 값은 API 호출 시 동작에 대한 설명으로 사용됩니다.

        구현 요구사항:
            - 이 속성은 반드시 JSON 형태로 이루어져야 합니다.
            - 각 key에 대한 설명과 타입을 지정해야 합니다.

        참고 문서:
            Opena AI 공식 문서 : https://platform.openai.com/docs/guides/function-calling
        """
        pass

    @property
    @abstractmethod
    def system_content(self) -> str:
        """
        Chat GPT의 역할을 저장하는 변수입니다.

        해당 속성은 상속 받은 클래스에서 반드시 구현되어야 합니다.
        속성의 값은 API 호출 시 반환된 값으로 사용됩니다.

        구현 요구사항:
            - 이 속성은 반드시 문자열 형태로 이루어져야 합니다.
        """
        pass

    @property
    @abstractmethod
    def question(self) -> str:
        """
        Chat GPT에 전달할 질문을 지정하는 변수입니다.

        해당 속성은 상속 받은 클래스에서 반드시 구현되어야 합니다.
        속성의 값은 API 호출 시 질문으로 사용됩니다.

        구현 요구사항:
            - 이 속성은 반드시 문자열 형태로 이루어져야 합니다.
        """
        pass

    @abstractmethod
    def parse_answer(self, completion: ChatCompletion) -> dict:
        """
        Chat GPT의 반환 값을 파싱하는 메소드입니다.

        해당 메소드는 상속 받은 클래스에서 반드시 구현되어야 합니다.
        get_answer를 통해 반환된 값을 파싱하여 반환합니다.

        구현 요구사항:
            - 이 메소드는 반드시 반환 값을 지정해야 합니다.
            - 반환 값은 API 호출 시 반환된 값과 동일한 타입이어야 합니다.
            - 반드시, function_description에 명시된 key를 사용하여 반환 값을 지정해야 합니다.

        :param completion: Chat GPT의 반환 값입니다.
        :return: Chat GPT의 반환 값을 파싱한 값입니다.
        """
        pass

    def get_answer(self) -> dataclass():
        """
        Chat GPT를 사용하여 질문에 대한 답변을 반환하는 메소드입니다.

        기본적으로, Chat GPT 4o-mini 모델을 사용하며, 질문에 대한 답변을 반환합니다.

        주의 사항:
            - 해당 메소드는 반드시 JSON 형태로 반환 됩니다.
            - 반환 값은 구현 메소드(parse_answer)를 통해 자식 클래스에서 구현되어야 합니다.
            - 구현 메소드(parse_answer)를 참고하여, 반환 값의 형태를 숙지해야 합니다.

        :return: Chat GPT를 사용하여 반환된 답변입니다.
        """
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    'role': 'system',
                    'content': self.system_content
                },
                {
                    'role': 'user',
                    'content': self.question
                }
            ],
            functions=self.function_description,
            function_call='auto',
            response_format={'type': 'json_object'},
            temperature=0.7,
            top_p=1
        )

        return self.parse_answer(completion)
