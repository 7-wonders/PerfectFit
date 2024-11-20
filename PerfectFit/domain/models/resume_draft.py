from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, CHAR, BOOLEAN, TIMESTAMP
from sqlalchemy import ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.app_user import AppUser
    from domain.models.job import Job
    from domain.models.keyword import Keyword
    from domain.models.pros_cons import ProsCons
    from domain.models.resume_section import ResumeSection


class ResumeDraft(db.Model):
    __tablename__ = "resume_draft"

    draft_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    job_id: Mapped[Optional[int]] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("job.job_id", onupdate="CASCADE", ondelete="SET NULL")
    )
    level: Mapped[Optional[str]] = mapped_column(CHAR(2))
    title: Mapped[Optional[str]] = mapped_column(VARCHAR(80))
    directional: Mapped[Optional[str]] = mapped_column(VARCHAR(1000))
    is_shared: Mapped[Optional[bool]] = mapped_column(BOOLEAN, server_default="0")
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped["AppUser"] = db.relationship("AppUser", back_populates="resumeDrafts")
    job: Mapped["Job"] = db.relationship("Job", back_populates="resumeDrafts")
    resume_sections: Mapped[list["ResumeSection"]] = db.relationship("ResumeSection", back_populates="resumeDraft")
    pros_cons: Mapped[list["ProsCons"]] = db.relationship("ProsCons", back_populates="resumeDraft")
    keywords: Mapped[list["Keyword"]] = db.relationship("Keyword", back_populates="resumeDraft")

    __table_args__ = (
        CheckConstraint("level IN ('신입', '경력', '없음')", name="check_level"),
    )
