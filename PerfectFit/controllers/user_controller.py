from dataclasses import asdict
import json
from flask import Blueprint, render_template, request, Response

from dto.ProjectExperience.projectExperience import PexDTO
from dto.user.user import UserDto
from services.user_service import UserService, ResumeService, InterviewService

user_bp = Blueprint('user', __name__)

def get_pagination_params():
    """공통적으로 페이지네이션 파라미터를 가져오는 함수"""
    page = request.args.get('page', default=1, type=int)
    count = request.args.get('count', default=10, type=int)
    return page, count

@user_bp.route('/users')
def get_users():
    page, count = get_pagination_params()  # 페이지네이션 파라미터 함수 사용

    paginate_user = UserService.get_users(page, count)
    response: UserDto.Response.Users = UserDto.Response.Users(
        users=[UserDto.Response.IntroUser(user.user_id, user.username) for user in paginate_user.items],
        pages=paginate_user.pages,
    )

    return render_template("users.html", users=asdict(response))

@user_bp.route('/user/<user_id>')
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    response: UserDto.Response.IntroUser = UserDto.Response.IntroUser(user.id, user.name)
    return render_template("user.html", user=response)

@user_bp.route('/user/mypage/info')
def get_info():
    user_id = request.headers.get("user_id")
    user = UserService.get_user(user_id)

    response: PexDTO.Response.DetailedUser = PexDTO.Response.DetailedUser(
        user_id=user.id,
        username=user.name,
        age=user.age,
        major=user.major,
        university=user.university,
        university_status=user.university_status,
        grade=user.grade,
        address=user.address,
        detail_address=user.detail_address,
        email=user.email,
        phone_number=user.phone_number,
        profile_path=user.profile_path,
        work_experiences=[
            PexDTO.Response.WorkExperience(
                work_experience_id=exp.work_experience_id,
                from_date=exp.from_date,
                to_date=exp.to_date,
                company_name=exp.company_name,
                position=exp.position,
                responsibility=exp.responsibility
            )
            for exp in user.work_experiences
        ],
        project_experiences=[
            PexDTO.Response.ProjectExperience(
                project_experience_id=proj.project_experience_id,
                project_name=proj.project_name,
                from_date=proj.from_date,
                to_date=proj.to_date,
                contents=[
                    PexDTO.Response.ProjectExperienceContent(
                        project_experience_task_id=task.project_experience_task_id,
                        content=task.content
                    )
                    for task in proj.contents
                ]
            )
            for proj in user.project_experiences
        ]
    )

    json_response = json.dumps(asdict(response), ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@user_bp.route('/user/profile')
def get_profile():
    user_id = request.headers.get("user_id")  # 헤더에서 user_id 가져오기
    user = UserService.get_user(user_id)

    response = {
        "profilePath": user.profile_path
    }

    json_response = json.dumps(response, ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@user_bp.route('/user/mypage/resume')
def get_resumes():
    user_id = request.headers.get("user_id")
    page, count = get_pagination_params()

    user = UserService.get_user(user_id)
    resumes, total = ResumeService.get_resumes(user_id, page, count)

    response = {
        "user": {
            "userId": user.id,
            "username": user.name,
            "profilePath": user.profile_path
        },
        "resumes": [
            {
                "resumeId": resume.resume_id,
                "title": resume.title,
                "viewCount": resume.view_count,
                "likeCount": resume.like_count,
                "occupation": {
                    "occupationId": resume.occupation_id,
                    "occupationName": resume.occupation_name
                },
                "job": resume.job,
                "level": resume.level,
                "createdTime": resume.created_time
            }
            for resume in resumes
        ],
        "total": total
    }

    json_response = json.dumps(response, ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')

@user_bp.route('/user/mypage/interview')
def get_interviews():
    user_id = request.headers.get("user_id")
    page, count = get_pagination_params()

    user = UserService.get_user(user_id)
    interviews, total = InterviewService.get_interviews(user_id, page, count)

    response = {
        "user": {
            "userId": user.id,
            "username": user.name,
            "profilePath": user.profile_path
        },
        "interviews": [
            {
                "interviewId": interview.interview_id,
                "title": interview.title,
                "isPublic": interview.is_public,
                "viewCount": interview.view_count,
                "likeCount": interview.like_count,
                "occupation": {
                    "occupationId": interview.occupation_id,
                    "occupationName": interview.occupation_name
                },
                "job": interview.job,
                "level": interview.level,
                "createdTime": interview.created_time
            }
            for interview in interviews
        ],
        "total": total
    }

    json_response = json.dumps(response, ensure_ascii=False, indent=2)
    return Response(json_response, status=200, content_type='application/json; charset=utf-8')