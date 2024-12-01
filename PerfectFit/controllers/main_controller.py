from flask import Blueprint, render_template

from dto.main.main import MainDto
from services.main_service import MainService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    response: list[MainDto.Response.Population] = MainService.get_population_by_data()
    return render_template('main.html', response=response)
