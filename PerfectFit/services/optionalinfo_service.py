from domain.models import ProjectExperience, WorkExperience
from domain.models.app_user import AppUser
from config.config_mysql import get_session

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