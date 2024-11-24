from dataclasses import dataclass


class KeywordDto:
    class Request:
        @dataclass
        class Update:
            keywordId: int
            content: str

    class Response:
        @dataclass
        class Keyword:
            keywordId: int
            content: str
