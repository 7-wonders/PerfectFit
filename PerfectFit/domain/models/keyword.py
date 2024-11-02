from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.job import Job
    from domain.models.resume import Resume


class Keyword(db.Model):
    __tablename__ = "keyword"

    keyword_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    resume_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("resume.resume_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    job_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("job.job_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    content: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    # 관계 설정
    resume: Mapped["Resume"] = db.relationship("Resume", back_populates="keywords")
    job: Mapped["Job"] = db.relationship("Job", back_populates="keywords")
