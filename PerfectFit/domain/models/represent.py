from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy import func, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.company import Company
    from domain.models.job import Job


class Represent(db.Model):
    __tablename__ = "represent"

    represent_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("company.company_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    job_id: Mapped[int] = mapped_column(
        INTEGER(unsigned=True),
        ForeignKey("job.job_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    # 관계 설정
    company: Mapped["Company"] = db.relationship("Company", back_populates="represent")
    job: Mapped["Job"] = db.relationship("Job", back_populates="represent")