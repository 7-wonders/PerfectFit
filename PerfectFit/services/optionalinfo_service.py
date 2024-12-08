from domain.models import ProjectExperience, WorkExperience, ProjectExperienceTask
from domain.models.app_user import AppUser
from config.config_mysql import get_session

class OptionalInfoService:
    @staticmethod
    def register_info(user_id: int, major: str, university: str, university_status: str,
                      grade: str, project_experiences: list, work_experiences: list, phone_number: str):

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
    def register_projectexp(user_id: int, major: str, university: str, university_status: str,
                      grade: str, project_experiences: list, work_experiences: list, phone_number: str):

        with get_session() as session:
            # 사용자의 선택 정보를 업데이트합니다.
            user = session.query(AppUser).filter(AppUser.user_id == user_id).first()

            if user:

                user.project_experiences.clear()  # 기존 프로젝트 경험 삭제
                new_projects = []
                for project in project_experiences:
                    new_project = ProjectExperience(
                        user_id=user_id,
                        project_name=project["projectName"],
                        from_date=project["fromDate"],
                        to_date=project["toDate"],
                    )
                    session.add(new_project)
                    new_projects.append(new_project)
                    # user_id
                    session.flush()  # ID를 얻기 위해 flush() 호출 None
                    # 각 content를 ProjectExperienceTask로 생성
                    for content in project["contents"]:  # contents는 str[] 형태
                        new_task = ProjectExperienceTask(
                            project_experience_id=new_project.project_experience_id,
                            content=content,
                        )
                        session.add(new_task)
                session.commit()

    @staticmethod
    def register_workexp(user_id: int, major: str, university: str, university_status: str,
                      grade: str, project_experiences: list, work_experiences: list, phone_number: str):

        with get_session() as session:
            # 사용자의 선택 정보를 업데이트합니다.
            user = session.query(AppUser).filter(AppUser.user_id == user_id).first()

            if user:
                # 직장 경험 정보 업데이트
                user.work_experiences.clear()  # 기존 직장 경험 삭제
                for work in work_experiences:
                    new_work = WorkExperience(
                        user_id=user_id,
                        company_name=work["companyName"],
                        from_date=work["fromDate"],
                        to_date=work["toDate"],
                        position=work["position"],
                        responsibility=work["responsibility"],
                        reason=work["reason"]
                    )
                    session.add(new_work)

                session.commit()