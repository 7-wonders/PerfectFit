from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy.dialects.mysql import INTEGER, TEXT, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.interview_question import InterviewQuestion


class InterviewImprovement(db.Model):
    __tablename__ = "interview_improvement"

    improvement_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("interview_question.question_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    answer: Mapped[str] = mapped_column(TEXT, nullable=False)
    improvement: Mapped[str] = mapped_column(TEXT, nullable=False)
    translated_answer: Mapped[str] = mapped_column(TEXT, nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    question: Mapped["InterviewQuestion"] = db.relationship("InterviewQuestion", back_populates="interview_improvements")
