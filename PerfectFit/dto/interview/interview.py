from dataclasses import dataclass
from pydantic import BaseModel
from typing import List

from dto.company_best.company_best import CompanyBestDto


class InterviewDto:
    class Request:
        @dataclass
        class PostInterviewAnswer:
            questionIds: list[int]
            answers: list[str]
              
        @dataclass
        class PostMakeInterviewResume:
            resumeId: int
            level: str
            title: str

        @dataclass
        class PostMakeInterviewJob:
            jobId: int
            userId: int
            level: str
            title: str
              
        @dataclass
        class PatchInterviewTitle:
            interviewId: int
            title: str

        @dataclass
        class SpellCheck:
            content: str


    class Response:
        @dataclass
        class InterviewQuestion:
            interview_id: int
            question_id: int
            question: str

        @dataclass
        class Questions:
            questions: list['InterviewDto.Response.InterviewQuestion']
            total: int

        @dataclass
        class IsPublicInterview:
            questionId: int
            title: str
            answer: str
            isPublic: bool

        @dataclass
        class IsPublicList:
            interviews: list['InterviewDto.Response.IsPublicInterview']

        @dataclass
        class QuestionList:
            questions: list['InterviewDto.Response.InterviewQuestion']
            total: int

        @dataclass
        class Improvement:
            improvementId: int
            questionId: int
            question: str
            answer: str
            improvement: str
            translatedAnswer: str

        # 새로 추가된 interviewSummary
        @dataclass
        class InterviewSummary:
            interview_id: int
            title: str
            created_time: str
            view_count: int
            like_count: int

        class InterviewQuestionAnswer(BaseModel):
            Question: str
            BestAnswer: str

        class InterviewResponse(BaseModel):
            InterviewQuestions: List['InterviewDto.Response.InterviewQuestionAnswer']

        @dataclass
        class CompanyInterviewResponse:
            interviewId: int
            companyName: str
            level: str
            title: str
            jobName: str
            university: str
            companyBest: list[CompanyBestDto.Response.CompanyBest]
            companyWorst: str

        @dataclass
        class JobInterviewResponse:
            interviewId: int
            companyName: str
            level: str
            title: str
            jobName: str
            university: str