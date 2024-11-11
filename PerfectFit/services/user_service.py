from flask import flash, abort
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy.orm import joinedload
from sqlalchemy.testing.requirements import Requirements

from database.config import get_session
from domain.models import ResumeLike, Interview, ProjectExperience, WorkExperience
from domain.models.app_user import AppUser
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType

from sqlalchemy.sql import func
from domain.models.resume import Resume
from domain.models.resume_view import ResumeView


class UserService:
    @staticmethod
    def get_users(page: int, count: int) -> Pagination:
        paginate_user = AppUser.query.paginate(page=page, per_page=count, error_out=False)
        return paginate_user

    @staticmethod
    def get_user(user_id: int) -> AppUser | None:
        user: AppUser = get_session().query(AppUser).options(
            joinedload(AppUser.project_experience)
        ).filter(AppUser.user_id == user_id).first()

        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        # project_experience를 변수에 담기
        project_experiences = user.project_experience  # SQLAlchemy 관계로 가져온 데이터

        return user

class ResumeService:
    @staticmethod
    def get_resumes(user_id: int, page: int, count: int):
        session = get_session()

        # 자기소개서 목록을 가져오기 위한 쿼리
        resumes_query = session.query(Resume).filter(Resume.user_id == user_id)
        total = resumes_query.count()

        resumes = resumes_query.order_by(Resume.created_time.desc()) \
                               .offset((page - 1) * count) \
                               .limit(count) \
                               .all()

        # 조회수 및 좋아요 수 계산
        for resume in resumes:
            resume.view_count = session.query(func.sum(ResumeView.view_count)).filter(
                ResumeView.resume_id == resume.resume_id
            ).scalar() or 0

            resume.like_count = session.query(func.sum(ResumeLike.like_count)).filter(
                ResumeLike.resume_id == resume.resume_id
            ).scalar() or 0

        return resumes, total

class InterviewService:
    @staticmethod
    def get_interviews(user_id: int, page: int, count: int):
        session = get_session()

        # 면접 데이터를 가져오는 쿼리 정의
        interviews_query = session.query(Interview).filter(Interview.user_id == user_id)
        total = interviews_query.count()

        interviews = interviews_query.order_by(Interview.created_time.desc()) \
            .offset((page - 1) * count) \
            .limit(count) \
            .all()

        # 조회수 및 좋아요 수 계산
        for interview in interviews:
            interview.view_count = session.query(func.sum(ResumeView.view_count)).filter(
                ResumeView.resume_id == interview.interview_id
            ).scalar() or 0

            interview.like_count = session.query(func.sum(ResumeLike.like_count)).filter(
                ResumeLike.resume_id == interview.interview_id
            ).scalar() or 0

        return interviews, total

class RequirementsService:
    @staticmethod
    def create_requirements(user_id: int, keywords: list, job_id: int, level: str, pros: str, cons: str, prompt: str, title: list):
        session = get_session()

        # 새 Requirements 인스턴스 생성 및 데이터베이스에 저장
        requirements = Requirements(
            user_id=user_id,
            keywords=keywords,
            job_id=job_id,
            level=level,
            pros=pros,
            cons=cons,
            prompt=prompt,
            title=title
        )

        session.add(requirements)
        session.commit()

class NecessaryInfoService:
    @staticmethod
    def register_info(user_id: int, name: str, age: int, email: str, address: str, detail_address: str):
        session = get_session()

        # 사용자의 필수 정보를 업데이트 또는 삽입합니다.
        necessary_info = session.query(AppUser).filter(AppUser.user_id == user_id).first()

        if necessary_info:
            # 정보가 이미 존재하는 경우 업데이트
            necessary_info.name = name
            necessary_info.age = age
            necessary_info.email = email
            necessary_info.address = address
            necessary_info.detail_address = detail_address
        else:
            # 새로운 사용자 정보를 추가
            new_info = AppUser(
                user_id=user_id,
                name=name,
                age=age,
                email=email,
                address=address,
                detail_address=detail_address
            )
            session.add(new_info)

        session.commit()

class OptionalInfoService:
    @staticmethod
    def register_info(user_id: int, major: str, university: str, university_status: str,
                      grade: float, project_experiences: list, work_experiences: list, phone_number: str):
        session = get_session()

        # 사용자의 선택 정보를 업데이트합니다.
        user = session.query(AppUser).filter(AppUser.user_id == user_id).first()

        if user:
            # 기본 필드 업데이트
            user.major = major
            user.university = university
            user.university_status = university_status
            user.grade = grade
            user.phone_number = phone_number

            # 프로젝트 경험 정보 업데이트
            user.project_experience.clear()  # 기존 프로젝트 경험 삭제
            for project in project_experiences:
                new_project = ProjectExperience(
                    user_id=user_id,
                    project_name=project["projectName"],
                    from_date=project["fromDate"],
                    to_date=project["toDate"],
                    contents=project["contents"]
                )
                session.add(new_project)

            # 직장 경험 정보 업데이트
            user.work_experience.clear()  # 기존 직장 경험 삭제
            for work in work_experiences:
                new_work = WorkExperience(
                    user_id=user_id,
                    company_name=work["company_name"],
                    from_date=work["fromDate"],
                    to_date=work["toDate"],
                    position=work["position"],
                    responsibility=work["responsibility"],
                    reason=work["reason"]
                )
                session.add(new_work)

            session.commit()

import smtplib
from email.mime.text import MIMEText
import random
import redis  # Redis 쓰신다고 하셨던 것이 기억나서, Redis 사용하는 방향으로 한번 작성해보았습니다!

# Redis 클라이언트 초기화
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class VerificationService:
    @staticmethod
    def generate_verification_code():
        """6자리 숫자로 구성된 인증 코드를 생성합니다."""
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_verification_code(email: str):
        verification_code = VerificationService.generate_verification_code()

        # 이메일 전송 설정
        smtp_server = "smtp.example.com"  # 실제 SMTP 서버 주소로 변경
        smtp_port = 587
        smtp_username = "your_email@example.com"  # 실제 이메일로 변경
        smtp_password = "your_password"  # 실제 비밀번호로 변경

        # 이메일 내용 구성
        subject = "Your Verification Code"
        body = f"Your verification code is: {verification_code}"
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = smtp_username
        message["To"] = email

        # SMTP 서버에 연결하여 이메일 전송
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, email, message.as_string())

        # 인증 코드를 Redis에 저장하고 유효 기간을 5분(300초)으로 설정
        redis_client.setex(f"verification_code:{email}", 300, verification_code)

    @staticmethod
    def verify_code(email: str, code: str) -> bool:
        """입력한 인증 코드가 유효한지 검증합니다."""
        # Redis에서 인증 코드 가져오기
        saved_code = redis_client.get(f"verification_code:{email}")

        # 코드가 존재하지 않거나 일치하지 않으면 False 반환
        if saved_code is None:
            return False

        if saved_code == code:
            # 인증 성공 후 Redis에서 해당 인증 코드 삭제
            redis_client.delete(f"verification_code:{email}")
            return True
        else:
            return False

class UserService:
    @staticmethod
    def delete_user(user_id: int):
        session = get_session()

        # 사용자 조회
        user = session.query(AppUser).filter(AppUser.user_id == user_id).first()
        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        # 사용자 삭제 (Hard Delete)
        session.delete(user)
        session.commit()