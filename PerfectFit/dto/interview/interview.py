from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional


class InterviewDto:
    class Request:
        @dataclass
        class postInterviewAnswer:
            questionId: int
            answer: str
              
        @dataclass
        class postMakeInterviewResume:
            resumeId: int
            level: str

        @dataclass
        class postMakeInterviewJob:
            jobId: int
            userId: int
            level: str
              
        @dataclass
        class patchInterviewTitle:
            interviewId: int
            title: str

        @dataclass
        class spellCheck:
            content: str

        @dataclass
        class isPublicIds:
            questionIds: list[int]

    class Response:
        @dataclass
        class interview:
            interview_id: int
            user_id: int
            resume_id: int
            job_id: int
            company_id: int
            title: str
            level: str

        @dataclass
        class interviewQuestion:
            question_id: int
            question: str

        @dataclass
        class questions:
            questions: list['InterviewDto.Response.interviewQuestion']
            total: int

        @dataclass
        class isPublicInterview:
            questionId: int
            title: str
            answer: str
            isPublic: bool

        @dataclass
        class isPublicList:
            interviews: list['InterviewDto.Response.isPublicInterview']

        @dataclass
        class improvement:
            improvementId: int
            questionId: int
            answer: str
            improvement: str
            translatedAnswer: str

        @dataclass
        class improvementList:
            improvements: list['InterviewDto.Response.improvement']

        @dataclass
        class spellChecked:
            translatedContent: str

        # 새로 추가된 interviewSummary
        @dataclass
        class interviewSummary:
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
