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

