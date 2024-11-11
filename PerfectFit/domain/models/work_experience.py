from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, DATE, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.app_user import AppUser


class WorkExperience(db.Model):
    __tablename__ = "work_experience"

    work_experience_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    company_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    from_date: Mapped[str] = mapped_column(DATE, nullable=False)
    to_date: Mapped[str] = mapped_column(DATE, nullable=False)
    reason: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    position: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    responsibility: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped["AppUser"] = db.relationship("AppUser", back_populates="work_experience")
