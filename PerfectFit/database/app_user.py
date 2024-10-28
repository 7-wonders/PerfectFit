from typing import Optional, List

from database.config import Base

from sqlalchemy import CheckConstraint, func
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TINYINT, DECIMAL, TIMESTAMP, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.project_experience import ProjectExperience
from database.resume import Resume
from database.resume_like import ResumeLike
from database.work_experience import WorkExperience


class AppUser(Base):
    __tablename__ = "app_user"

    user_id: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True)
    sns_id: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    sns_kind: Mapped[str] = mapped_column(CHAR(4), nullable=False)
    username: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    age: Mapped[int] = mapped_column(TINYINT, nullable=False)
    major: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    job: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    address: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    detail_address: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(VARCHAR(11))
    university: Mapped[Optional[str]] = mapped_column(VARCHAR(30))
    university_status: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    grade: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 2))
    email: Mapped[Optional[str]] = mapped_column(VARCHAR(50))
    profile_path: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    profile_size: Mapped[Optional[int]] = mapped_column(INTEGER(unsigned=True))
    profile_type: Mapped[Optional[str]] = mapped_column(VARCHAR(10))
    created_time: Mapped[Optional[str]] = mapped_column(TIMESTAMP, server_default=func.now())

    work_experience: Mapped[List[WorkExperience]] = relationship("WorkExperience", back_populates="user")
    project_experience: Mapped[List[ProjectExperience]] = relationship("ProjectExperience", back_populates="user")
    resumes: Mapped[list[Resume]] = relationship("Resume", back_populates="user")
    resume_likes: Mapped[list[ResumeLike]] = relationship("ResumeLike", back_populates="user")

    __table_args__ = {
        # 1001: Naver, 1002: Google, 1003: Kakao
        CheckConstraint("sns_kind IN ('1001', '1002', '1003')", name="check_sns_kind"),
        CheckConstraint("university_status IN ('재학', '중퇴', '졸업예정', '졸업')", name="check_university_status"),
    }
