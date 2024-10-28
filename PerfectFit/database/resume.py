from typing import Optional

from database.app_user import AppUser
from database.config import Base

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, CHAR, BOOLEAN, TIMESTAMP
from sqlalchemy import ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.job import Job
from database.resume_like import ResumeLike
from database.resume_section import ResumeSection


class Resume(Base):
    __tablename__ = "resume"

    resume_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    job_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("job.job_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    level: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    title: Mapped[str] = mapped_column(VARCHAR(80), nullable=False)
    is_draft: Mapped[Optional[bool]] = mapped_column(BOOLEAN, server_default="0")
    is_shared: Mapped[Optional[bool]] = mapped_column(BOOLEAN, server_default="0")
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped[AppUser] = relationship("AppUser", back_populates="resumes")
    job: Mapped[Job] = relationship("Job", back_populates="resumes")
    resume_sections: Mapped[list[ResumeSection]] = relationship("ResumeSection", back_populates="resume")
    resume_likes: Mapped[list[ResumeLike]] = relationship("ResumeLike", back_populates="resume")

    __table_args__ = (
        CheckConstraint("level IN ('신입', '경력', '없음')", name="check_level"),
    )
