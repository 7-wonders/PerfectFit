from flask import request, flash
from sqlalchemy import select, literal, func

from config.config_mysql import get_session
from domain.models import Job, ProsCons, Keyword, ResumeSection, Occupation
from domain.models.resume_draft import ResumeDraft
from dto.keyword.keyword import KeywordDto
from dto.resume.resume import ResumeDto
from dto.resume_draft.resume_draft import ResumeDraftDto
from dto.resume_section.resume_section import ResumeSectionDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from utils.jwt_factory import JWTFactory


class ResumeDraftService:
    @staticmethod
    def get_draft(draft_id: str):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

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
                raise CustomException(ExceptionType.NOT_FOUND_RESUME)

            if draft.get('userId') != user_id:
                raise CustomException(ExceptionType.FORBIDDEN_RESUME)

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

            response = ResumeDraftDto.Response.DraftForWrite(
                resume=ResumeDraftDto.Response.DraftWithWrite(
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
                jobs=[dict(job) for job in jobs] if jobs else None,
                occupations=[dict(occupation) for occupation in occupations]
            )

            return response

    @staticmethod
    def add_draft(data: ResumeDraftDto.Request.Create):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            count_query = (
                select(func.count(ResumeDraft.draft_id))
                .where(ResumeDraft.user_id == user_id)
            )

            count = session.execute(count_query).scalar()
            if count >= 10:
                flash('자기소개서는 최대 10개까지 작성할 수 있습니다.', 'danger')
                return

            if data.job_id:
                job = session.query(Job).filter(Job.job_id == data.job_id).first()
                if not job:
                    raise CustomException(ExceptionType.NOT_FOUND_JOB)

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

    @staticmethod
    def update_draft(draft_id: str, data: ResumeDto.Request.Update):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with (get_session() as session):
            draft = session.query(ResumeDraft).filter(ResumeDraft.draft_id == draft_id).first()
            if not draft:
                raise CustomException(ExceptionType.INVALID_DRAFT_ID)

            if draft.user_id != user_id:
                raise CustomException(ExceptionType.FORBIDDEN_RESUME)

            if data.job_id:
                job = session.query(Job).filter(Job.job_id == data.job_id).first()
                if not job:
                    raise CustomException(ExceptionType.INVALID_JOB_ID)

                draft.job_id = data.job_id

            draft.title = data.title
            draft.level = data.level
            draft.directional = data.directional
            draft.is_shared = data.is_shared

            pros = session.query(ProsCons).filter(ProsCons.draft_id == draft_id, ProsCons.type == 'pros').first()

            if pros and (not data.pros or not data.pros.strip()):
                session.delete(pros)
            elif pros:
                pros.content = data.pros
            else:
                pros = ProsCons(
                    draft_id=draft_id,
                    type='pros',
                    content=data.pros
                )
                session.add(pros)

            cons = session.query(ProsCons).filter(ProsCons.draft_id == draft_id, ProsCons.type == 'cons').first()
            if cons and (not data.cons or not data.cons.strip()):
                session.delete(cons)
            elif cons:
                cons.content = data.cons
            else:
                cons = ProsCons(
                    draft_id=draft_id,
                    type='cons',
                    content=data.cons
                )
                session.add(cons)

            session.query(Keyword).filter(Keyword.draft_id == draft_id).delete()
            if data.keywords:
                keywords = [
                    Keyword(
                        draft_id=draft_id,
                        job_id=data.job_id,
                        content=keyword.content
                    )
                    for keyword in data.keywords
                ]
                session.add_all(keywords)

            db_section = session.query(ResumeSection).filter(ResumeSection.draft_id == draft_id).all()

            if data.sections and len(data.sections) > 0:
                new_sections = []

                # 사용자가 추가한 섹션 ID 기준으로 나누기
                data_sections_by_id = {int(section.section_id): section
                                       for section in data.sections
                                       if section.section_id not in [None, "None", "", "null"]}
                # DB에 저장된 섹션 ID 기준으로 나누기
                db_sections = {section.resume_section_id: section
                               for section in db_section}
                # 사용자가 추가한 섹션
                new_sections_by_data = [section
                                        for section in data.sections
                                        if section.section_id in [None, "None", "", "null"]]

                db_sections_ids = set(db_sections.keys())
                data_sections_ids = set(data_sections_by_id.keys())

                # 사용자가 추가한 섹션 ID가 DB에 저장된 섹션 ID에 포함되지 않았다면 삭제
                for section_id in db_sections_ids - data_sections_ids:
                    session.delete(db_sections[section_id])

                # 사용자가 추가한 섹션 ID가 DB에 저장된 섹션 ID에 포함되어 있다면 수정
                for section_id in db_sections_ids & data_sections_ids:
                    db_section = db_sections[section_id]
                    db_section.title = data_sections_by_id[section_id].title
                    db_section.content = data_sections_by_id[section_id].content

                # 사용자가 추가한 섹션 ID가 DB에 저장된 섹션 ID에 포함되지 않았다면 추가
                for section in new_sections_by_data:
                    new_sections.append(ResumeSection(
                        draft_id=draft_id,
                        title=section.title,
                        content=section.content
                    ))

                session.add_all(new_sections)
            else:
                session.query(ResumeSection).filter(ResumeSection.draft_id == draft_id).delete()

            session.commit()

    @staticmethod
    def delete_draft(draft_id: str):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            draft = session.query(ResumeDraft).filter(ResumeDraft.draft_id == draft_id).first()
            if not draft:
                raise CustomException(ExceptionType.INVALID_DRAFT_ID)

            if draft.user_id != user_id:
                raise CustomException(ExceptionType.FORBIDDEN_RESUME)

            session.query(ResumeSection).filter(ResumeSection.draft_id == draft_id).delete(synchronize_session='fetch')
            session.query(Keyword).filter(Keyword.draft_id == draft_id).delete(synchronize_session='fetch')
            session.query(ProsCons).filter(ProsCons.draft_id == draft_id, ProsCons.type == 'pros').delete()
            session.query(ProsCons).filter(ProsCons.draft_id == draft_id, ProsCons.type == 'cons').delete()

            session.delete(draft)
            session.commit()
