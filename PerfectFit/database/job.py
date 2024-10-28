from typing import Optional

from database.config import Base

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.occupation import Occupation
from database.resume import Resume


class Job(Base):
    __tablename__ = "job"

    job_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    occupation_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("occupation.occupation_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    job_name: Mapped[str] = mapped_column(VARCHAR(80), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    occupation: Mapped[Occupation] = relationship("Occupation", back_populates="jobs")
    resumes: Mapped[list[Resume]] = relationship("Resume", back_populates="job")
