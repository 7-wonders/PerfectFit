from flask import Blueprint, request

from dto.resume_draft.resume_draft import ResumeDraftDto
from dto.resume_section.resume_section import ResumeSectionDto
from logs.log import Logger
from services.resume_draft_service import ResumeDraftService

resume_draft_bp = Blueprint('resume_draft_bp', __name__)
logger = Logger(__name__)

@resume_draft_bp.route('/', methods=['POST'])
def add_draft():
    title = request.form.get("title")
    job_id = request.form.get("job_id")
    level = request.form.get("level")
    pros = request.form.get("pros")
    cons = request.form.get("cons")
    is_shared = request.form.get("is_shared") or False
    directional = request.form.get("directional")
    keywords = request.form.getlist("keywords[]")
    section_titles = request.form.getlist("sections[][title]")
    section_contents = request.form.getlist("sections[][content]")
    sections = zip(section_titles, section_contents)

    ResumeDraftService.add_draft(ResumeDraftDto.Request.Create(
        title=title,
        job_id=int(job_id),
        level=level,
        pros=pros,
        cons=cons,
        is_shared=is_shared,
        directional=directional,
        keywords=keywords,
        sections=[ResumeSectionDto.Request.Create(title=title, content=content)
                  for title, content in sections]
    ))

