from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, CHAR, TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.job import Job
    from domain.models.competencies import Competencies


class Occupation(db.Model):
    __tablename__ = "occupation"

    occupation_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    occupation_name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    major_category: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    sub_category: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    jobs: Mapped[list["Job"]] = db.relationship("Job", back_populates="occupation")
    competencies: Mapped[list["Competencies"]] = db.relationship("Competencies", back_populates="occupation")