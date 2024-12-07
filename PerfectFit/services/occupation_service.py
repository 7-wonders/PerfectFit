from sqlalchemy import select

from config.config_mysql import get_session
from domain.models import Occupation


class OccupationService:
    @staticmethod
    def get_occupations():
        with get_session() as session:
            query = (
                select(
                    Occupation.occupation_id.label('occupationId'),
                    Occupation.occupation_name.label('occupationName')
                )
            )

            occupations = session.execute(query).mappings().all()

            return occupations