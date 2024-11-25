from sqlalchemy.testing.requirements import Requirements
from config.config_mysql import get_session

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
