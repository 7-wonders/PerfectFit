from typing import Optional, TYPE_CHECKING

from database.config import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.company import Company


class CompanyBest(db.Model):
    __tablename__ = "company_best"

    best_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    company_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("company.company_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    content: Mapped[str] = mapped_column(VARCHAR(40), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    # 관계 설정
    company: Mapped["Company"] = db.relationship("Company", back_populates="company_bests")
