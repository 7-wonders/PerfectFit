from dataclasses import dataclass


class JobDto:
    class Response:
        @dataclass
        class JobInfo:
            job_id: int
            job_name: str

        @dataclass
        class Jobs:
            jobs: list['JobDto.Response.JobInfo']

        @dataclass
        class OccupationInfo:
            occupation_id: int
            occupation_name: str
            major_category: str
            sub_category: str
        @dataclass
        class Occupations:
            occupations: list['JobDto.Response.OccupationInfo']