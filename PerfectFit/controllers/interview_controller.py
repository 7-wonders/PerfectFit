
from flask import Blueprint, render_template


interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/loading')
def loading_create():
    return render_template("Loading-create.html")


@interview_bp.route('/loading-analyze')
def loading_analyze():
    return render_template("Loading-analyze.html")


@interview_bp.route('/')
def interview():
    return render_template("interview.html")


@interview_bp.route('/list')
def interviewlist():
    return render_template("interviewlist.html")


@interview_bp.route('/result')
def result():
    return render_template("result.html")