from typing import Optional

from database.app_user import AppUser
from database.config import Base

from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.resume import Resume


class ResumeLike(Base):
    __tablename__ = "resume_like"

    like_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
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

    # 관계 설정 (optional)
    resume: Mapped[Resume] = relationship("Resume", back_populates="resume_likes")
    user: Mapped[AppUser] = relationship("AppUser", back_populates="resume_likes")
