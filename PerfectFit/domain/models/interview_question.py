from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BOOLEAN, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column


if TYPE_CHECKING:
    from domain.models.interview import Interview
    from domain.models.interview_improvement import InterviewImprovement
    from domain.models import InterviewAnswer


class InterviewQuestion(db.Model):
    __tablename__ = "interview_question"

    question_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    interview_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("interview.interview_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    question: Mapped[str] = mapped_column(VARCHAR(300), nullable=False)
    is_shared: Mapped[Optional[bool]] = mapped_column(BOOLEAN, server_default="0")
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    interview: Mapped["Interview"] = db.relationship("Interview", back_populates="interview_questions")
    interview_answers: Mapped[list["InterviewAnswer"]] = db.relationship("InterviewAnswer", back_populates="question")
    interview_improvements: Mapped[list["InterviewImprovement"]] = db.relationship("InterviewImprovement",
                                                                              back_populates="question")
