from typing import Optional, List, TYPE_CHECKING

from database.config import db

from sqlalchemy import CheckConstraint, func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TINYINT, DECIMAL, TIMESTAMP, CHAR
from sqlalchemy.orm import Mapped, mapped_column


if TYPE_CHECKING:
    from domain.models.interview import Interview
    from domain.models.interview_like import InterviewLike
    from domain.models.interview_view import InterviewView
    from domain.models.project_experience import ProjectExperience
    from domain.models.resume import Resume
    from domain.models.resume_like import ResumeLike
    from domain.models.resume_view import ResumeView
    from domain.models.work_experience import WorkExperience


class AppUser(db.Model):
    __tablename__ = "app_user"

    user_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    sns_id: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    sns_kind: Mapped[str] = mapped_column(CHAR(4), nullable=False)
    username: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    age: Mapped[int] = mapped_column(TINYINT)
    major: Mapped[str] = mapped_column(VARCHAR(30))
    job: Mapped[str] = mapped_column(VARCHAR(30))
    address: Mapped[str] = mapped_column(VARCHAR(100))
    detail_address: Mapped[str] = mapped_column(VARCHAR(50))
    phone_number: Mapped[Optional[str]] = mapped_column(VARCHAR(11))
    university: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    university_status: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    grade: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 2))
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    profile_path: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    profile_size: Mapped[Optional[int]] = mapped_column(INTEGER(unsigned=True))
    profile_type: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    work_experience: Mapped[List["WorkExperience"]] = db.relationship("WorkExperience", back_populates="user")
    project_experience: Mapped[List["ProjectExperience"]] = db.relationship("ProjectExperience", back_populates="user")
    resumes: Mapped[list["Resume"]] = db.relationship("Resume", back_populates="user")
    resume_likes: Mapped[list["ResumeLike"]] = db.relationship("ResumeLike", back_populates="user")
    resume_views: Mapped[list["ResumeView"]] = db.relationship("ResumeView", back_populates="user")
    interviews: Mapped[list["Interview"]] = db.relationship("Interview", back_populates="user")
    interview_views: Mapped[list["InterviewView"]] = db.relationship("InterviewView", back_populates="user")
    interview_likes: Mapped[list["InterviewLike"]] = db.relationship("InterviewLike", back_populates="user")

    __table_args__ = (
        # 1001: Naver, 1002: Google, 1003: Kakao
        CheckConstraint("sns_kind IN ('1001', '1002', '1003')", name="check_sns_kind"),
        CheckConstraint("university_status IN ('재학', '중퇴', '졸업예정', '졸업')", name="check_university_status"),
    )
