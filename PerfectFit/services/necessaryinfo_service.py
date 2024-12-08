from flask import request
from sqlalchemy import select

from domain.models import WorkExperience, ProjectExperience, ProjectExperienceTask
from domain.models.app_user import AppUser
from config.config_mysql import get_session
from dto.project_experience.project_experience import PexDTO
from dto.user.user import UserDto
from dto.work_experience.work_experience import WorkExperienceDTO
from utils.jwt_factory import JWTFactory


class NecessaryInfoService:
    @staticmethod
    def get_info() -> UserDto.Response.NecessaryInfo:
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            user_query = (
                select(
                    AppUser.user_id.label('userId'),
                    AppUser.username,
                    AppUser.age,
                    AppUser.address,
                    AppUser.detail_address.label('detailAddress'),
                    AppUser.email
                )
                .where(AppUser.user_id == user_id)
            )

            user_info = session.execute(user_query).mappings().first()

            return UserDto.Response.NecessaryInfo(
                username=user_info['username'],
                age=user_info['age'],
                email=user_info['email'],
                address=user_info['address'],
                detailAddress=user_info['detailAddress']
            )

    @staticmethod
    def get_optional_info() -> UserDto.Response.OptionalInfo:
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            user_query = (
                select(
                    AppUser.user_id.label('userId'),
                    AppUser.major,
                    AppUser.university,
                    AppUser.university_status,
                    AppUser.grade,
                    AppUser.phone_number
                )
                .where(AppUser.user_id == user_id)
            )

            user = session.execute(user_query).mappings().first()

            work_experience_query = (
                select(
                    WorkExperience.work_experience_id.label('workExperienceId'),
                    WorkExperience.company_name.label('companyName'),
                    WorkExperience.position,
                    WorkExperience.reason,
                    WorkExperience.responsibility,
                    WorkExperience.from_date.label('fromDate'),
                    WorkExperience.to_date.label('toDate'),
                )
                .where(WorkExperience.user_id == user_id)
            )

            work_experiences = session.execute(work_experience_query).mappings().all()

            project_experiences_query = (
                select(
                    ProjectExperience.project_experience_id.label('projectExperienceId'),
                    ProjectExperience.project_name.label('projectName'),
                    ProjectExperience.from_date.label('fromDate'),
                    ProjectExperience.to_date.label('toDate'),
                )
                .where(ProjectExperience.user_id == user_id)
            )

            project_experiences = session.execute(project_experiences_query).mappings().all()

            # 프로젝트 경험 과제 쿼리 실행
            tasks_query = (
                select(
                    ProjectExperienceTask.project_experience_id,
                    ProjectExperienceTask.content
                )
                .join(ProjectExperience,
                      ProjectExperience.project_experience_id == ProjectExperienceTask.project_experience_id)
                .where(ProjectExperience.user_id == user_id)
            )

            tasks_data = session.execute(tasks_query).mappings().all()

            tasks_dict = {}
            for task in tasks_data:
                project_experience_id = task['project_experience_id']
                if project_experience_id not in tasks_dict:
                    tasks_dict[project_experience_id] = []
                tasks_dict[project_experience_id].append(task['content'])

            return UserDto.Response.OptionalInfo(
                major=user['major'],
                university=user['university'],
                university_status=user['university_status'],
                grade=user['grade'],
                phone_number=user['phone_number'],
                project_experiences=[
                    PexDTO.Response.ProjectExperience(
                        projectExperienceId=project['projectExperienceId'],
                        projectName=project['projectName'],
                        fromDate=project['fromDate'],
                        toDate=project['toDate'],
                        contents=tasks_dict.get(project['projectExperienceId'], [])
                    )
                    for project in project_experiences
                ],
                work_experiences=[
                    WorkExperienceDTO.Response.WorkExperience(
                        workExperienceId=work['workExperienceId'],
                        companyName=work['companyName'],
                        position=work['position'],
                        fromDate=work['fromDate'],
                        toDate=work['toDate'],
                        reason=work['reason'],
                        responsibility=work['responsibility'],
                    )
                    for work in work_experiences
                ],
            )

    @staticmethod
    def register_info(user_id: int, name: str, age: int, email: str, address: str, detail_address: str):
        with get_session() as session :
            # 사용자의 필수 정보를 업데이트 또는 삽입합니다.
            necessary_info = session.query(AppUser).filter(AppUser.user_id == user_id).first()

            if necessary_info:
                # 정보가 이미 존재하는 경우 업데이트
                necessary_info.username = name
                necessary_info.age = age
                necessary_info.email = email
                necessary_info.address = address
                necessary_info.detail_address = detail_address
                session.add(necessary_info)
            else:
                # 새로운 사용자 정보를 추가
                new_info = AppUser(
                    user_id=user_id,
                    username=name,
                    age=age,
                    email=email,
                    address=address,
                    detail_address=detail_address
                )
                session.add(new_info)

            session.commit()
