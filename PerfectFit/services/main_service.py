from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from sqlalchemy.sql import expression

from config.config_mysql import get_session
from domain.models import ResumeSection, Resume, ResumeLike, ResumeView, Occupation, Job, AppUser, InterviewView, \
    InterviewLike, Interview, InterviewQuestion, InterviewImprovement
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
        view_scalar_query_interview = (
            select(func.count(InterviewView.view_id))
            .where(InterviewView.interview_id == Interview.interview_id)
            .scalar_subquery()
        )

        like_scalar_query_interview = (
            select(func.count(InterviewLike.like_id))
            .where(InterviewLike.interview_id == Interview.interview_id)
            .scalar_subquery()
        )

        one_section_scalar_query = (
            select(
                ResumeSection.title.label("sectionTitle"),
                ResumeSection.content.label("sectionContent"),
            )
            .where(ResumeSection.resume_id == Resume.resume_id)
            .limit(1)
            .lateral()
        )
        one_section_title_query = (
            select(ResumeSection.title)
            .where(ResumeSection.resume_id == Resume.resume_id)
            .order_by(ResumeSection.resume_id)
            .limit(1)
            .scalar_subquery()
        )

        one_section_content_query = (
            select(ResumeSection.content)
            .where(ResumeSection.resume_id == Resume.resume_id)
            .order_by(ResumeSection.resume_id)
            .limit(1)
            .scalar_subquery()
        )

        resume_query = (
            select(
                Resume.resume_id,
                Resume.title,
                Resume.level,
                view_scalar_query.label("viewCount"),
                like_scalar_query.label("likeCount"),
                one_section_title_query.label("sectionTitle"),
                one_section_content_query.label("sectionContent"),
                # one_section_scalar_query.c.sectionTitle,
                # one_section_scalar_query.c.sectionContent,
                Occupation.occupation_name.label("occupationName"),
                Job.job_name.label("jobName"),
                AppUser.username.label("username"),
            )
            .join(Job, Job.job_id == Resume.job_id)
            .join(Occupation, Occupation.occupation_id == Job.occupation_id)
            .join(AppUser, AppUser.user_id == Resume.user_id)
            .where(Resume.is_shared.is_(True))
            .order_by(view_scalar_query.desc(), like_scalar_query.desc(), Resume.created_time.desc())
            .limit(2)
        )
        with get_session() as session:
            resumes = session.execute(resume_query).mappings().all()

            resume_response: list[MainDto.Response.Population] = [

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
                )
                for resume in resumes
            ]

            valid_interviews = []  # 조건을 만족하는 인터뷰를 담을 리스트
            offset = 0  # 가져온 인터뷰의 시작 위치
            limit = 4  # 가져올 인터뷰 개수
            question_alias = aliased(InterviewQuestion)
            improvement_alias = aliased(InterviewImprovement)

            # 4개의 유효한 인터뷰를 찾을 때까지 반복
            while len(valid_interviews) < 4:
                # 1. viewCount 내림차순으로 인터뷰 가져오기
                interview_query = (
                    select(
                        Interview.interview_id,
                        Interview.title,
                        Interview.level,
                        view_scalar_query_interview.label("viewCount"),
                        like_scalar_query_interview.label("likeCount"),
                        Occupation.occupation_name.label("occupationName"),
                        Job.job_name.label("jobName")
                    )
                    .join(Job, Job.job_id == Interview.job_id)
                    .join(Occupation, Occupation.occupation_id == Job.occupation_id)
                    .order_by(view_scalar_query_interview.desc())
                    .offset(offset)
                    .limit(limit)
                )

                interviews = session.execute(interview_query).mappings().all()

                if not interviews:
                    break  # 더 이상 인터뷰가 없다면 반복 종료

                # 가져온 인터뷰 중에서 유효한 인터뷰만 필터링
                for interview in interviews:
                    # 2. 해당 interview에서 is_shared가 True인 질문이 1개라도 있는지 검사
                    question_query = (
                        select(question_alias)
                        .where(question_alias.interview_id == interview["interview_id"])
                        .where(question_alias.is_shared == True)
                    )
                    shared_questions = session.execute(question_query).scalars().all()

                    # 3. 만약 is_shared가 True인 질문이 없다면 해당 interview 제외하고 다음 인터뷰로 넘어감
                    if not shared_questions:
                        continue

                    # 4. is_shared가 True인 질문이 있으면 그 중 하나를 선택하고 질문과 답변을 할당
                    first_question = shared_questions[0]  # 첫 번째 질문을 선택
                    improvement_answer = (
                        session.execute(
                            select(improvement_alias.answer)
                            .where(improvement_alias.question_id == first_question.question_id)
                        )
                        .scalars()
                        .first()
                    )
                    if improvement_answer is None :
                        continue

                    interview_json = {
                        "interviewId": interview["interview_id"],
                        "title": interview["title"],
                        "level": interview["level"],
                        "viewCount": interview["viewCount"],
                        "likeCount": interview["likeCount"],
                        "occupationName": interview["occupationName"],
                        "jobName": interview["jobName"],
                        "question": first_question.question,
                        "answer": improvement_answer if improvement_answer else "No answer available"
                    }
                    valid_interviews.append(interview_json)
                    if len(valid_interviews) >= 4:
                        break
                # 다음 배치의 인터뷰를 가져오기 위해 offset을 갱신
                offset += limit
            return resume_response, valid_interviews
