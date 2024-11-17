from flask import Blueprint, render_template

resume_bp = Blueprint('resume', __name__)


@resume_bp.route('/write/part')
def get_resume_write_part():
    return render_template("resume_write_part.html")

@resume_bp.route('/write/all')
def get_resume_write_all():
    return render_template("resume_write_all.html")

@resume_bp.route('/select')
def get_resume_select():
    return render_template("resume_select.html")

@resume_bp.route('/information/all')
def get_resume_information_all():
    return render_template("resume_information_all.html")

@resume_bp.route('/information/part')
def get_resume_information_part():
    return render_template("resume_information_part.html")

@resume_bp.route('/loading')
def get_resume_load_loading():
    return render_template("resume_loading.html")

@resume_bp.route('/list/<int:page>')
def get_resume_list(page):
    totalItems = 100  # 예시: 전체 항목의 수
    pageRange = 5  # 한 번에 표시할 페이지 범위
    totalPages = (totalItems + pageRange - 1) // pageRange  # 전체 페이지 수 계산
    return render_template("resume_list.html", page=page, totalPages=totalPages, pageRange=pageRange)

@resume_bp.route('/detail')
def get_resume_detail():
    page = 1;
    totalItems = 100  # 예시: 전체 항목의 수
    pageRange = 5  # 한 번에 표시할 페이지 범위
    totalPages = (totalItems + pageRange - 1) // pageRange  # 전체 페이지 수 계산
    return render_template("resume_detail.html", page=page, totalPages=totalPages, pageRange=pageRange)