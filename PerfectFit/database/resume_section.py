from typing import Optional

from database.config import Base

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.resume import Resume


class ResumeSection(Base):
    __tablename__ = "resume_section"

    resume_section_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    resume_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("resume.resume_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(VARCHAR(60), nullable=False)
    content: Mapped[str] = mapped_column(TEXT, nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    resume: Mapped[Resume] = relationship("Resume", back_populates="resume_sections")
