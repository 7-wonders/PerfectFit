from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATE, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.app_user import AppUser
    from domain.models.project_experience_task import ProjectExperienceTask


class ProjectExperience(db.Model):
    __tablename__ = "project_experience"

    project_experience_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True
    )
    from_date: Mapped[str] = mapped_column(DATE, nullable=False)
    to_date: Mapped[str] = mapped_column(DATE, nullable=False)
    project_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped["AppUser"] = db.relationship("AppUser", back_populates="project_experiences")
    tasks: Mapped[list["ProjectExperienceTask"]] = db.relationship("ProjectExperienceTask",
                                                              back_populates="project_experience")
