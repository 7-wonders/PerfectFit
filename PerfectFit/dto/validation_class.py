from abc import ABC, abstractmethod


class FormModel(ABC):
    @abstractmethod
    def __validation__(self) -> str:
        """
        모든 FormModel 클래스는 해당 메소드를 통해 데이터 유효성 검증을 시도합니다.
        :return: 유효성 검증 실패 시 메시지를 반환합니다.
        """
        pass
