
from sqlalchemy.sql import func
from domain.models import ResumeLike
from domain.models.resume import Resume
from domain.models.resume_view import ResumeView
from config.config_mysql import get_session

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