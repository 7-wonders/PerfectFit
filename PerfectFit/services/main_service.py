from sqlalchemy import select, func

from config.config_mysql import get_session
from domain.models import ResumeSection, Resume, ResumeLike, ResumeView, Occupation, Job, AppUser
from dto.main.main import MainDto
from dto.resume_section.resume_section import ResumeSectionDto


class MainService:
    @staticmethod
    def get_population_by_data():
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

        one_section_scalar_query = (
            select(
                ResumeSection.title.label("sectionTitle"),
                ResumeSection.content.label("sectionContent"),
            )
            .where(ResumeSection.resume_id == Resume.resume_id)
            .limit(1)
            .subquery()
        )

        resume_query = (
            select(
                Resume.resume_id,
                Resume.title,
                Resume.level,
                view_scalar_query.label("viewCount"),
                like_scalar_query.label("likeCount"),
                one_section_scalar_query,
                Occupation.occupation_name.label("occupationName"),
                Job.job_name.label("jobName"),
                AppUser.username.label("username"),
            )
            .join(ResumeSection, ResumeSection.resume_id == Resume.resume_id)
            .join(Job, Job.job_id == Resume.job_id)
            .join(Occupation, Occupation.occupation_id == Job.occupation_id)
            .join(AppUser, AppUser.user_id == Resume.user_id)
            .order_by(view_scalar_query.desc(), like_scalar_query.desc(), Resume.created_time.desc())
            .limit(2)
        )

        with get_session() as session:
            resumes = session.execute(resume_query).mappings().all()

            response: list[MainDto.Response.Population] = [
                MainDto.Response.Population(
                    resumeId=resume["resume_id"],
                    title=resume["title"],
                    level=resume["level"],
                    viewCount=resume["viewCount"],
                    likeCount=resume["likeCount"],
                    occupationName=resume["occupationName"],
                    jobName=resume["jobName"],
                    username=resume["username"],
                    section=ResumeSectionDto.Response.Section(
                        title=resume["sectionTitle"],
                        content=resume["sectionContent"],
                    ),
                    interviews=[]
                )
                for resume in resumes
            ]

            return response
