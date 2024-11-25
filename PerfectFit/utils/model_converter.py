from datetime import datetime

from sqlalchemy import RowMapping


def model_to_dict(dt: RowMapping) -> dict:
    new_dict = {}

    for key, value in dt.items():
        if isinstance(value, datetime):
            new_dict[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        else:
            new_dict[key] = value

    return new_dict
