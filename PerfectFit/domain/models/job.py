from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.interview import Interview
    from domain.models.keyword import Keyword
    from domain.models.occupation import Occupation
    from domain.models.resume import Resume


class Job(db.Model):
    __tablename__ = "job"

    job_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    occupation_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("occupation.occupation_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    job_name: Mapped[str] = mapped_column(VARCHAR(80), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    occupation: Mapped["Occupation"] = db.relationship("Occupation", back_populates="jobs")
    resumes: Mapped[list["Resume"]] = db.relationship("Resume", back_populates="job")
    keywords: Mapped[list["Keyword"]] = db.relationship("Keyword", back_populates="job")
    interviews: Mapped[list["Interview"]] = db.relationship("Interview", back_populates="job")
