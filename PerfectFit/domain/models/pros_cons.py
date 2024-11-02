from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, CHAR, VARCHAR, TIMESTAMP
from sqlalchemy import ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.resume import Resume


class ProsCons(db.Model):
    __tablename__ = "pros_cons"

    pros_cons_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    resume_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("resume.resume_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    type: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    content: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    resume: Mapped["Resume"] = db.relationship("Resume", back_populates="pros_cons")

    # 제약 조건 설정
    __table_args__ = (
        CheckConstraint("type IN ('장점', '단점')", name="check_type"),
    )
