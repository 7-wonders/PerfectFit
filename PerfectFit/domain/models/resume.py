from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, CHAR, BOOLEAN, TIMESTAMP
from sqlalchemy import ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.app_user import AppUser
    from domain.models.interview import Interview
    from domain.models.job import Job
    from domain.models.keyword import Keyword
    from domain.models.pros_cons import ProsCons
    from domain.models.resume_like import ResumeLike
    from domain.models.resume_section import ResumeSection
    from domain.models.resume_view import ResumeView


class Resume(db.Model):
    __tablename__ = "resume"

    resume_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    job_id: Mapped[Optional[int]] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("job.job_id", onupdate="CASCADE", ondelete="SET NULL")
    )
    level: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    title: Mapped[str] = mapped_column(VARCHAR(80), nullable=False)
    directional: Mapped[Optional[str]] = mapped_column(VARCHAR(1000))
    is_shared: Mapped[Optional[bool]] = mapped_column(BOOLEAN, server_default="0")
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped["AppUser"] = db.relationship("AppUser", back_populates="resumes")
    job: Mapped["Job"] = db.relationship("Job", back_populates="resumes")
    resume_sections: Mapped[list["ResumeSection"]] = db.relationship("ResumeSection", back_populates="resume")
    resume_likes: Mapped[list["ResumeLike"]] = db.relationship("ResumeLike", back_populates="resume")
    resume_views: Mapped[list["ResumeView"]] = db.relationship("ResumeView", back_populates="resume")
    pros_cons: Mapped[list["ProsCons"]] = db.relationship("ProsCons", back_populates="resume")
    keywords: Mapped[list["Keyword"]] = db.relationship("Keyword", back_populates="resume")
    interviews: Mapped[list["Interview"]] = db.relationship("Interview", back_populates="resume")

    __table_args__ = (
        CheckConstraint("level IN ('신입', '경력', '없음')", name="check_level"),
    )
