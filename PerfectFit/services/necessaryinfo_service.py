from domain.models.app_user import AppUser
from config.config_mysql import get_session


class NecessaryInfoService:
    @staticmethod
    def register_info(user_id: int, name: str, age: int, email: str, address: str, detail_address: str):
        with get_session() as session :
            # 사용자의 필수 정보를 업데이트 또는 삽입합니다.
            necessary_info = session.query(AppUser).filter(AppUser.user_id == user_id).first()
            print(necessary_info)
            if necessary_info:
                # 정보가 이미 존재하는 경우 업데이트
                necessary_info.username = name
                necessary_info.age = age
                necessary_info.email = email
                necessary_info.address = address
                necessary_info.detail_address = detail_address
                session.add(necessary_info)
            else:
                # 새로운 사용자 정보를 추가
                new_info = AppUser(
                    user_id=user_id,
                    username=name,
                    age=age,
                    email=email,
                    address=address,
                    detail_address=detail_address
                )
                session.add(new_info)

            session.commit()