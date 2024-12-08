from domain.models.project_experience import ProjectExperience
from domain.models.project_experience_task import ProjectExperienceTask
from domain.models.work_experience import WorkExperience
from domain.models.app_user import AppUser
from config.config_mysql import get_session

class OptionalInfoService:
    @staticmethod
    def register_info(user_id: int, major: str, university: str, university_status: str,
                      grade: str, phone_number: str):

        with get_session() as session:
            # 사용자의 선택 정보를 업데이트합니다.
            user = session.query(AppUser).filter(AppUser.user_id == user_id).first()

            if user:
                # 기본 필드 업데이트
                user.major = major
                user.university = university
                user.university_status = university_status
                user.grade = grade
                user.phone_number = phone_number
                session.commit()

    @staticmethod
    def register_projectexp(user_id: int, project_experiences: list):

        with get_session() as session:
            # 사용자의 선택 정보를 업데이트합니다.
            user = session.query(AppUser).filter(AppUser.user_id == user_id).first()

            for project in user.project_experiences:
                for task in project.tasks:
                    session.delete(task)
                session.delete(project)

            for project in project_experiences:
                # 프로젝트 경험 객체 생성
                new_project = ProjectExperience(
                    user_id=int(user_id),
                    project_name=str(project["projectName"]),
                    from_date=str(project["fromDate"]),
                    to_date=str(project["toDate"]),
                )

                session.add(new_project)
                session.flush()

                for content in project["contents"]:
                    new_task = ProjectExperienceTask(
                        project_experience_id=int(new_project.project_experience_id),
                        content=str(content),
                    )
                    session.add(new_task)

            session.commit()

    @staticmethod
    def register_workexp(user_id: int, work_experiences: list):

        with get_session() as session:
            # 사용자의 선택 정보를 업데이트합니다.
            user = session.query(AppUser).filter(AppUser.user_id == user_id).first()

            for work in user.work_experiences:
                session.delete(work)

            for work in work_experiences:
                new_work = WorkExperience(
                    user_id=int(user_id),
                    company_name=str(work["companyName"]),
                    from_date=str(work["fromDate"]),
                    to_date=str(work["toDate"]),
                    position=str(work["position"]),
                    responsibility=str(work["responsibility"]),
                    reason=str(work["reason"])
                )
                session.add(new_work)

            session.commit()