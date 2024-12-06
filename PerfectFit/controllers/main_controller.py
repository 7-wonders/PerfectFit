from flask import Blueprint, render_template

from dto.main.main import MainDto
from services.main_service import MainService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    resume_response, interview_response = MainService.get_population_by_data()
    response = MainDto.Response.MainPopulation(resume_response, interview_response)
    return render_template('main.html', response=response)
