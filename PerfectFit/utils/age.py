import datetime


def get_age(birth_year: int, birth_month: int, birth_day: int) -> int:
    current_day = datetime.datetime.now()
    birth_day = datetime.datetime(birth_year, birth_month, birth_day)

    # 생일이 지났는지 확인
    if current_day.month >= birth_day.month and current_day.day >= birth_day.day:
        return current_day.year - birth_day.year

    return current_day.year - birth_day.year - 1
