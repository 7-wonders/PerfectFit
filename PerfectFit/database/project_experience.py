from database.app_user import AppUser
from database.config import Base

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATE, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProjectExperience(Base):
    __tablename__ = "project_experience"

    project_experience_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    from_date: Mapped[str] = mapped_column(DATE, nullable=False)
    to_date: Mapped[str] = mapped_column(DATE, nullable=False)
    project_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    created_time: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped[AppUser] = relationship("AppUser", back_populates="project_experience")
