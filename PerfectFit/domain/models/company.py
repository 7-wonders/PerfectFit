from typing import Optional, TYPE_CHECKING

from config.config_mysql import db

from sqlalchemy import func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

if TYPE_CHECKING:
    from domain.models.company_best import CompanyBest
    from domain.models.company_worst import CompanyWorst
    from domain.models.interview import Interview
    from domain.models.interview_like import InterviewLike
    from domain.models.interview_view import InterviewView
    from domain.models.represent import Represent


class Company(db.Model):
    __tablename__ = "company"

    company_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    company_name: Mapped[str] = mapped_column(VARCHAR(300), nullable=False)
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    interviews: Mapped[list["Interview"]] = db.relationship("Interview", back_populates="company")
    interview_views: Mapped[list["InterviewView"]] = db.relationship("InterviewView", back_populates="company")
    interview_likes: Mapped[list["InterviewLike"]] = db.relationship("InterviewLike", back_populates="company")
    company_bests: Mapped[list["CompanyBest"]] = db.relationship("CompanyBest", back_populates="company")
    company_worsts: Mapped[list["CompanyWorst"]] = db.relationship("CompanyWorst", back_populates="company")
    represent: Mapped["Represent"] = db.relationship("Represent", back_populates="company")
