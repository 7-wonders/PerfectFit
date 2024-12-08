from http import HTTPStatus

from flask import Blueprint, request, redirect, url_for, flash, jsonify

from dto.keyword.keyword import KeywordDto
from dto.resume.resume import ResumeDto
from dto.resume_draft.resume_draft import ResumeDraftDto
from dto.resume_section.resume_section import ResumeSectionDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from logs.log import Logger
from services.resume_draft_service import ResumeDraftService

resume_draft_bp = Blueprint('resume_draft', __name__)
logger = Logger(__name__)


@resume_draft_bp.route('/<draft_id>', methods=['GET'])
def get_draft(draft_id: str):
    if not draft_id or not draft_id.isdigit():
        raise CustomException(ExceptionType.INVALID_RESUME_ID)

    draft = ResumeDraftService.get_draft(draft_id)
    return jsonify(draft), 200


@resume_draft_bp.route('/', methods=['POST'])
def add_draft():
    request_json = request.get_json()
    title = request_json.get("title")
    job_id = request_json.get("jobId")
    level = request_json.get("level")
    pros = request_json.get("pros")
    cons = request_json.get("cons")
    is_shared = request_json.get("isShared") or False
    directional = request_json.get("directional")
    keywords = [
        keyword
        for keyword in request_json.get("keywords", None)
    ]
    sections = [
        ResumeSectionDto.Request.Create(
            title=section["title"],
            content=section["content"]
        )
        for section in request_json.get("sections", None)
    ]

    draft_id = ResumeDraftService.add_draft(ResumeDraftDto.Request.Create(
        title=title,
        job_id=int(job_id) if job_id else None,
        level=level,
        pros=pros,
        cons=cons,
        is_shared=bool(is_shared),
        directional=directional,
        keywords=keywords,
        sections=sections
    ))

    if not draft_id:
        raise CustomException(ExceptionType.INVALID_DRAFT_ID)

    return {"draftId": draft_id}, HTTPStatus.CREATED


@resume_draft_bp.route('/<draft_id>', methods=['POST'])
def update_draft(draft_id: str):
    if not draft_id or not draft_id.isdigit():
        raise CustomException(ExceptionType.INVALID_DRAFT_ID)

    request_json = request.get_json()

    data = ResumeDto.Request.Update(
        job_id=int(request_json.get("jobId", None)),
        title=request_json.get("title", None),
        level=request_json.get("level", None),
        pros=request_json.get("pros", None),
        cons=request_json.get("cons", None),
        is_shared=bool(request_json.get("isPublic") if request_json.get("isPublic") else False),
        directional=request_json.get("directional", None),
        keywords=[KeywordDto.Request.Update(
            keywordId=0,
            content=keyword)
            for keyword in request_json.get("keywords", None)]
        if request_json.get("keywords") else None,
        sections=[ResumeSectionDto.Request.Update(
            section_id=section.get("sectionId") if section.get("sectionId") else None,
            title=section.get("title") if section.get("title") else None,
            content=section.get("content") if section.get("content") else None
        )
        for section in request_json.get("sections", None)]
        if request_json.get("sections") else None
    )

    ResumeDraftService.update_draft(draft_id, data)
    return {}, HTTPStatus.NO_CONTENT


@resume_draft_bp.route('/<draft_id>', methods=['DELETE'])
def delete_draft(draft_id: str):
    if not draft_id or not draft_id.isdigit():
        raise CustomException(ExceptionType.INVALID_DRAFT_ID)

    ResumeDraftService.delete_draft(draft_id)
    return {}, HTTPStatus.NO_CONTENT
