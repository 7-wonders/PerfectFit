from dataclasses import asdict

from flask import Blueprint, request

from dto.resume.resume import ResumeDto
from exception.custom_exception import CustomException
from exception.exception_type import ExceptionType
from utils.openai.resume.full_resume_strategy import FullResumeStrategy
from utils.openai.resume.resume_helper import ResumeHelper
from utils.openai.resume.resume_strategy import CreateResume

resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/', methods=['POST'])
def create_resume():
    data = request.get_json()
    request_resume = ResumeDto.Request.CreateFullResume(**data)

    if not request_resume.keywords:
        return CustomException(ExceptionType.REQUIRED_KEYWORDS)
    elif not request_resume.job_id:
        return CustomException(ExceptionType.REQUIRED_JOB)
    elif not request_resume.level:
        return CustomException(ExceptionType.REQUIRED_LEVEL)
    elif not request_resume.pros:
        return CustomException(ExceptionType.REQUIRED_PROS)
    elif not request_resume.cons:
        return CustomException(ExceptionType.REQUIRED_CONS)

    helper = ResumeHelper(strategy=FullResumeStrategy(resume=CreateResume(
        keywords=request_resume.keywords,
        job_name='백엔드 개발자',
        level=request_resume.level,
        pros=request_resume.pros,
        cons=request_resume.cons,
        directional='',
        chapter=''
    )))

    return asdict(helper.get_answer())
