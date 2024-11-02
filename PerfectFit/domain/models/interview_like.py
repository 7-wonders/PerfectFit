from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.app_user import AppUser
    from domain.models.company import Company
    from domain.models.interview import Interview


class InterviewLike(db.Model):
    __tablename__ = "interview_like"

    like_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    interview_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("interview.interview_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("app_user.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    company_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("company.company_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    # 관계 설정
    interview: Mapped["Interview"] = db.relationship("Interview", back_populates="interview_likes")
    user: Mapped["AppUser"] = db.relationship("AppUser", back_populates="interview_likes")
    company: Mapped["Company"] = db.relationship("Company", back_populates="interview_likes")