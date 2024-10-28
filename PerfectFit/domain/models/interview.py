from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, CHAR, TIMESTAMP
from sqlalchemy import ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column


if TYPE_CHECKING:
    from domain.models.app_user import AppUser
    from domain.models.company import Company
    from domain.models.interview_like import InterviewLike
    from domain.models.interview_question import InterviewQuestion
    from domain.models.interview_view import InterviewView
    from domain.models.job import Job
    from domain.models.resume import Resume


class Interview(db.Model):
    __tablename__ = "interview"

    interview_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    resume_id: Mapped[Optional[int]] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("resume.resume_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True
    )
    job_id: Mapped[Optional[int]] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("job.job_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True
    )
    company_id: Mapped[Optional[int]] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("company.company_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True
    )
    title: Mapped[str] = mapped_column(VARCHAR(80), nullable=False)
    level: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped["AppUser"] = db.relationship("AppUser", back_populates="interviews")
    resume: Mapped[Optional["Resume"]] = db.relationship("Resume", back_populates="interviews")
    job: Mapped[Optional["Job"]] = db.relationship("Job", back_populates="interviews")
    company: Mapped[Optional["Company"]] = db.relationship("Company", back_populates="interviews")
    interview_questions: Mapped[list["InterviewQuestion"]] = db.relationship("InterviewQuestion", back_populates="interview")
    interview_views: Mapped[list["InterviewView"]] = db.relationship("InterviewView", back_populates="interview")
    interview_likes: Mapped[list["InterviewLike"]] = db.relationship("InterviewLike", back_populates="interview")

    __table_args__ = (
        CheckConstraint("level IN ('신입', '경력', '없음')", name="check_level"),
    )
