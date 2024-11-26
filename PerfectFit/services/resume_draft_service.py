from flask import request

from dto.resume_draft.resume_draft import ResumeDraftDto
from utils.jwt_factory import JWTFactory


class ResumeDraftService:
    @staticmethod
    def add_draft(data: ResumeDraftDto.Request.Create):
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

