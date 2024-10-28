from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, TEXT, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.project_experience import ProjectExperience


class ProjectExperienceTask(db.Model):
    __tablename__ = "project_experience_task"

    project_experience_task_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    project_experience_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("project_experience.project_experience_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    content: Mapped[str] = mapped_column(TEXT, nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    project_experience: Mapped["ProjectExperience"] = db.relationship("ProjectExperience", back_populates="tasks")
