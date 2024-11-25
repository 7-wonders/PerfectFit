from dataclasses import dataclass


class JobDto:
    class Response:
        @dataclass
        class JobInfo:
            jobId: int
            jobName: str

        @dataclass
        class Jobs:
            jobs: list['JobDto.Response.JobInfo']

        @dataclass
        class OccupationInfo:
            occupationId: int
            occupationName: str
            majorCategory: str
            subCategory: str
        @dataclass
        class OccupationInfoWithJob:
            occupationId: int
            occupationName: str
            majorCategory: str
            subCategory: str
            jobs: list['JobDto.Response.JobInfo'] = None
            total: int = 0
        @dataclass
        class Occupations:
            occupations: list['JobDto.Response.OccupationInfo']

        @dataclass
        class OccupationsWithJob:
            occupations: list['JobDto.Response.OccupationInfoWithJob']
