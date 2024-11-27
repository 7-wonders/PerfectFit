from flask import request, flash
from sqlalchemy import select, literal

from config.config_mysql import get_session
from domain.models import Job, ProsCons, Keyword, ResumeSection, Occupation
from domain.models.resume_draft import ResumeDraft
from dto.keyword.keyword import KeywordDto
from dto.resume_draft.resume_draft import ResumeDraftDto
from dto.resume_section.resume_section import ResumeSectionDto
from utils.jwt_factory import JWTFactory


class ResumeDraftService:
    @staticmethod
    def get_draft(draft_id: str):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))
        if not user_id:
            flash('로그인이 필요합니다.', 'danger')
            return None

        with (get_session() as session):
            pros_subquery = (
                select(ProsCons.content)
                .where(ProsCons.draft_id == draft_id)
                .where(ProsCons.type == 'pros')
                .scalar_subquery()
            )

            cons_subquery = (
                select(ProsCons.content)
                .where(ProsCons.draft_id == draft_id)
                .where(ProsCons.type == 'cons')
                .scalar_subquery()
            )

            draft_query = (
                select(
                    ResumeDraft.user_id.label('userId'),
                    ResumeDraft.draft_id.label('draftId'),
                    ResumeDraft.job_id.label('jobId'),
                    ResumeDraft.title,
                    ResumeDraft.level,
                    ResumeDraft.directional,
                    ResumeDraft.is_shared.label('isPublic'),
                    pros_subquery.label('pros'),
                    cons_subquery.label('cons')
                )
                .filter(ResumeDraft.draft_id == draft_id)
            )

            draft = session.execute(draft_query).mappings().first()

            if not draft:
                flash('자기소개서 정보를 불러오는 중 오류가 발생했습니다.', 'danger')
                return None

            if draft.get('userId') != user_id:
                flash('본인의 자기소개서만 수정할 수 있습니다.', 'danger')
                return None

            sections_query = (
                select(
                    ResumeSection.resume_section_id.label('sectionId'),
                    ResumeSection.title,
                    ResumeSection.content
                )
                .filter(ResumeSection.draft_id == draft_id)
            )

            sections = session.execute(sections_query).mappings().all()

            keywords_query = (
                select(
                    Keyword.keyword_id.label('keywordId'),
                    Keyword.content
                )
                .filter(Keyword.draft_id == draft_id)
            )

            keywords = session.execute(keywords_query).mappings().all()

            job_id = draft.get('jobId')

            if job_id:
                selected_job_query = (
                    select(
                        Job.occupation_id
                    )
                    .where(Job.job_id == job_id)
                    .scalar_subquery()
                )

                job_query = (
                    select(
                        Job.job_id.label('jobId'),
                        Job.job_name.label('jobName'),
                        (
                                Job.job_id == job_id
                        ).label('isSelected')
                    )
                    .where(
                        Job.occupation_id == selected_job_query
                    )
                )

            pros = draft.get('pros')
            cons = draft.get('cons')

            occupation_query = (
                select(
                    Occupation.occupation_id.label('occupationId'),
                    Occupation.occupation_name.label('occupationName'),
                    (
                            Occupation.occupation_id == selected_job_query if job_id else literal(False)
                    ).label('isSelected')
                )
            )

            jobs = (session.execute(job_query).mappings().all()
                    if job_id else None)
            occupations = session.execute(occupation_query).mappings().all()

            response = ResumeDraftDto.Response.DraftForUpdate(
                resume=ResumeDraftDto.Response.DraftWithUpdate(
                    draftId=draft.get('draftId'),
                    title=draft.get('title'),
                    level=draft.get('level'),
                    pros=pros,
                    cons=cons,
                    keywords=[
                        KeywordDto.Response.Keyword(
                            keywordId=keyword.get('keywordId'),
                            content=keyword.get('content')
                        )
                        for keyword in keywords
                    ],
                    directional=draft.get('directional'),
                    sections=[
                        ResumeSectionDto.Response.Section(
                            sectionId=section.get('sectionId'),
                            title=section.get('title'),
                            content=section.get('content')
                        )
                        for section in sections
                    ],
                    isPublic=draft.get('isPublic')
                ),
                jobs=jobs,
                occupations=occupations
            )

            return response

    @staticmethod
    def add_draft(data: ResumeDraftDto.Request.Create):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            if data.job_id:
                job = session.query(Job).filter(Job.job_id == data.job_id).first()
                if not job:
                    flash('선택된 직업이 존재하지 않습니다.', 'danger')
                    return

            draft = ResumeDraft(
                user_id=user_id,
                title=data.title,
                job_id=data.job_id,
                level=data.level,
                is_shared=data.is_shared,
                directional=data.directional,
            )

            session.add(draft)
            session.flush()

            pros = ProsCons(
                draft_id=draft.draft_id,
                type='pros',
                content=data.pros
            )

            cons = ProsCons(
                draft_id=draft.draft_id,
                type='cons',
                content=data.cons
            )

            session.add_all([pros, cons])

            if data.sections and len(data.sections) > 0:
                sections = [ResumeSection(draft_id=draft.draft_id, title=section.title, content=section.content)
                            for section in data.sections
                            if section.title.strip() and section.content.strip()]

                session.add_all(sections)

            keywords = []
            for keyword in data.keywords:
                if not keyword.strip():
                    continue

                keywords.append(Keyword(
                    draft_id=draft.draft_id,
                    job_id=data.job_id,
                    content=keyword,
                ))

            if len(keywords) > 0:
                session.add_all(keywords)

            session.commit()

            return draft.draft_id
