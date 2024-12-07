from flask import request, flash
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import select, func, case
from sqlalchemy.orm import joinedload
from sqlalchemy.testing.pickleable import User

from domain.models import Resume, ResumeView, ResumeLike, Job, Occupation, InterviewLike, Interview, InterviewView, \
    InterviewQuestion, WorkExperience, ProjectExperience, ProjectExperienceTask
from domain.models.app_user import AppUser
from dto.interview.interview import InterviewDto
from dto.occupation.occupation import OccupationDto
from dto.project_experience.project_experience import PexDTO
from dto.resume.resume import ResumeDto
from dto.user.user import UserDto
from dto.work_experience.work_experience import WorkExperienceDTO
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from config.config_mysql import get_session
from utils.jwt_factory import JWTFactory
from utils.model_converter import variable_to_date_string


class UserService:
    @staticmethod
    def get_users(page: int, count: int) -> Pagination:
        paginate_user = AppUser.query.paginate(page=page, per_page=count, error_out=False)
        return paginate_user

    @staticmethod
    def get_user() -> AppUser | None:
        # 이렇게 사용하면 좀 더 쉽게 사용하실 수 있습니다 !
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        user: AppUser = get_session().query(AppUser).options(
            joinedload(AppUser.project_experiences)
        ).filter(AppUser.user_id == user_id).first()

        if not user:
            raise CustomException(ExceptionType.NOT_FOUND_USER)

        return user

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

    @staticmethod
    def get_user_with_resumes(page: int, count: int) -> ResumeDto.Response.MyResume:
        """
        사용자 정보와 이력서를 함께 가져오는 메서드
        """
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            user_query = (
                select(
                    AppUser.user_id.label('userId'),
                    AppUser.username,
                    AppUser.profile_path.label('profilePath'),
                )
                .where(AppUser.user_id == user_id)
            )

            user = session.execute(user_query).mappings().first()

            if not user:
                flash('사용자 정보를 찾을 수 없습니다.', 'error')
                return None

            view_scalar_query = (
                select(func.count(ResumeView.view_id))
                .where(ResumeView.resume_id == Resume.resume_id)
                .scalar_subquery()
            )

            like_scalar_query = (
                select(func.count(ResumeLike.like_id))
                .where(ResumeLike.resume_id == Resume.resume_id)
                .scalar_subquery()
            )

            is_like_scalar_query = func.exists(
                select(1)
                .where(ResumeLike.user_id == user_id, ResumeLike.resume_id == Resume.resume_id)
            )

            resume_query = (
                select(
                    Resume.resume_id.label('resumeId'),
                    Resume.title,
                    Resume.level,
                    Resume.is_shared.label('isShared'),
                    like_scalar_query.label('likeCount'),
                    view_scalar_query.label('viewCount'),
                    is_like_scalar_query.label('isLike'),
                    Resume.created_time.label('createdTime'),
                    Job.job_name.label('jobName'),
                    Occupation.occupation_name.label('occupationName'),
                )
                .join(Job, Job.job_id == Resume.job_id)
                .join(Occupation, Occupation.occupation_id == Job.occupation_id)
                .where(Resume.user_id == user_id)
                .order_by(Resume.created_time.desc())
                .offset((page - 1) * count)
                .limit(count)
            )

            total_query = (
                select(func.count(Resume.resume_id))
                .where(Resume.user_id == user_id)
            )

            resumes = session.execute(resume_query).mappings().all()
            total = session.execute(total_query).scalar()

            return ResumeDto.Response.MyResume(
                user=UserDto.Response.IntroUserWithProfile(
                    userId=user.userId,
                    username=user.username,
                    profilePath=user.profilePath,
                ),
                resumes=[
                    ResumeDto.Response.MyResumeInfo(
                        resumeId=resume.resumeId,
                        title=resume.title,
                        viewCount=resume.viewCount,
                        likeCount=resume.likeCount,
                        isLike=resume.isLike,
                        occupationName=resume.occupationName,
                        jobName=resume.jobName,
                        level=resume.level,
                        isPublic=resume.isShared,
                        createdTime=variable_to_date_string(resume.createdTime),
                    )
                    for resume in resumes
                ],
                total=total,
            )

    @staticmethod
    def get_my_interviews(page: int, count: int) -> InterviewDto.Response.MyInterviews:
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            user_query = (
                select(
                    AppUser.user_id.label('userId'),
                    AppUser.username,
                    AppUser.profile_path.label('profilePath'),
                )
                .where(AppUser.user_id == user_id)
            )

            user = session.execute(user_query).mappings().first()

            if not user:
                flash('사용자 정보를 찾을 수 없습니다.', 'error')
                return None

            like_scalar_query = (
                select(func.count(InterviewLike.like_id))
                .where(InterviewLike.interview_id == Interview.interview_id)
                .scalar_subquery()
            )

            view_scalar_query = (
                select(func.count(InterviewView.view_id))
                .where(InterviewView.interview_id == Interview.interview_id)
                .scalar_subquery()
            )

            is_like_scalar_query = func.exists(
                select(1)
                .where(InterviewLike.user_id == user_id, InterviewLike.interview_id == Interview.interview_id)
                .scalar_subquery()
            )

            is_public_scalar_query = func.exists(
                select(1)
                .select_from(InterviewQuestion)
                .where(
                    InterviewQuestion.is_shared.is_(True),
                    InterviewQuestion.interview_id == Interview.interview_id
                )
                .scalar_subquery()
            )

            interview_query = (
                select(
                    Interview.interview_id.label('interviewId'),
                    Interview.title,
                    Interview.level,
                    like_scalar_query.label('likeCount'),
                    view_scalar_query.label('viewCount'),
                    is_like_scalar_query.label('isLike'),
                    Interview.created_time.label('createdTime'),
                    Occupation.occupation_name.label('occupationName'),
                    Job.job_name.label('jobName'),
                    is_public_scalar_query.label('isPublic'),
                )
                .join(Job, Job.job_id == Interview.job_id)
                .join(Occupation, Occupation.occupation_id == Job.occupation_id)
                .where(Interview.user_id == user_id)
                .order_by(Interview.created_time.desc())
                .offset((page - 1) * count)
                .limit(count)
            )

            total_query = (
                select(func.count(Interview.interview_id))
                .where(Interview.user_id == user_id)
            )

            interviews = session.execute(interview_query).mappings().all()
            total = session.execute(total_query).scalar()

            return InterviewDto.Response.MyInterviews(
                user=UserDto.Response.IntroUserWithProfile(
                    userId=user.userId,
                    username=user.username,
                    profilePath=user.profilePath,
                ),
                interviews=[
                    InterviewDto.Response.MyInterview(
                        interviewId=interview.interviewId,
                        title=interview.title,
                        level=interview.level,
                        viewCount=interview.viewCount,
                        likeCount=interview.likeCount,
                        isLike=interview.isLike,
                        occupationName=interview.occupationName,
                        jobName=interview.jobName,
                        isPublic=interview.isPublic,
                        createdTime=variable_to_date_string(interview.createdTime),
                    )
                    for interview in interviews
                ],
                total=total,
            )

    @staticmethod
    def get_information():
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            user_query = (
                select(
                    AppUser.user_id.label('userId'),
                    AppUser.username,
                    AppUser.age,
                    AppUser.major,
                    AppUser.university,
                    AppUser.university_status.label('universityStatus'),
                    AppUser.grade,
                    AppUser.address,
                    AppUser.detail_address.label('detailAddress'),
                    AppUser.email,
                    AppUser.phone_number.label('phoneNumber'),
                    AppUser.profile_path.label('profilePath'),
                )
                .where(AppUser.user_id == user_id)
            )

            user = session.execute(user_query).mappings().first()

            if not user:
                flash('사용자 정보를 찾을 수 없습니다.', 'error')
                return None

            work_experience_query = (
                select(
                    WorkExperience.work_experience_id.label('workExperienceId'),
                    WorkExperience.company_name.label('companyName'),
                    WorkExperience.from_date.label('fromDate'),
                    WorkExperience.to_date.label('toDate'),
                    WorkExperience.position,
                    WorkExperience.reason,
                    WorkExperience.responsibility
                )
                .where(WorkExperience.user_id == user_id)
            )

            work_experiences = session.execute(work_experience_query).mappings().all()

            project_query = (
                select(
                    ProjectExperience.project_experience_id.label('projectExperienceId'),
                    ProjectExperience.project_name.label('projectName'),
                    ProjectExperience.from_date.label('fromDate'),
                    ProjectExperience.to_date.label('toDate'),
                )
                .where(ProjectExperience.user_id == user_id)
            )

            project_experiences = session.execute(project_query).mappings().all()

            project_tasks_query = (
                select(
                    ProjectExperienceTask.project_experience_task_id.label('projectExperienceTaskId'),
                    ProjectExperienceTask.content,
                )
                .join(ProjectExperience, ProjectExperience.project_experience_id == ProjectExperienceTask.project_experience_id)
                .where(ProjectExperience.user_id == user_id)
            )

            project_tasks = session.execute(project_tasks_query).mappings().all()

            return UserDto.Response.DetailUser(
                user=UserDto.Response.UserDetail(
                    userId=user.userId,
                    username=user.username,
                    age=user.age,
                    major=user.major,
                    university=user.university,
                    universityStatus=user.universityStatus,
                    grade=user.grade,
                    address=user.address,
                    detailAddress=user.detailAddress,
                    email=user.email,
                    phoneNumber=user.phoneNumber,
                    profilePath=user.profilePath,
                ),
                work_experiences=[
                    WorkExperienceDTO.Response.WorkExperience(
                        workExperienceId=work_experience.workExperienceId,
                        companyName=work_experience.company,
                        fromDate=variable_to_date_string(work_experience.fromDate),
                        toDate=variable_to_date_string(work_experience.toDate),
                        position=work_experience.position,
                        reason=work_experience.reason,
                        responsibility=work_experience.responsibility,
                    )
                    for work_experience in work_experiences
                ],
                project_experiences=[
                    PexDTO.Response.ProjectExperience(
                        projectExperienceId=project_experience.projectExperienceId,
                        projectName=project_experience.projectName,
                        fromDate=variable_to_date_string(project_experience.fromDate),
                        toDate=variable_to_date_string(project_experience.toDate),
                        contents=[
                            PexDTO.Response.ProjectExperienceContent(
                                project_experience_task_id=project_task.projectExperienceTaskId,
                                content=project_task.content,
                            )
                            for project_task in project_tasks
                        ]
                    )
                    for project_experience in project_experiences
                ],
            )
