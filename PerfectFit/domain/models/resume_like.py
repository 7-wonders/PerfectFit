from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.app_user import AppUser
    from domain.models.resume import Resume


class ResumeLike(db.Model):
    __tablename__ = "resume_like"

    like_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    resume_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("resume.resume_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    resume: Mapped["Resume"] = db.relationship("Resume", back_populates="resume_likes")
    user: Mapped["AppUser"] = db.relationship("AppUser", back_populates="resume_likes")
