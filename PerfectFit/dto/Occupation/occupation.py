from dataclasses import dataclass


class OccupationDto:
    class Response:
        @dataclass
        class Occupation:
            occupationId: int
            occupationName: str
