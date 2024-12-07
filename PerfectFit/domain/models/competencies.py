from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.occupation import Occupation


class Competencies(db.Model):
    __tablename__ = "competencies"

    competencies_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    occupation_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("occupation.occupation_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    content: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    # 관계 설정
    occupation: Mapped["Occupation"] = db.relationship("Occupation", back_populates="competencies")
