from flask import request
from sqlalchemy import select

from domain.models.app_user import AppUser
from config.config_mysql import get_session
from dto.user.user import UserDto
from utils.jwt_factory import JWTFactory


class NecessaryInfoService:
    @staticmethod
    def get_info() -> UserDto.Response.NecessaryInfo:
        user_id = JWTFactory().verify_access_token(request.cookies.get('access_token'))

        with get_session() as session:
            user_query = (
                select(
                    AppUser.user_id.label('userId'),
                    AppUser.username,
                    AppUser.age,
                    AppUser.address,
                    AppUser.detail_address.label('detailAddress'),
                    AppUser.email
                )
                .where(AppUser.user_id == user_id)
            )

            user_info = session.execute(user_query).mappings().first()

            return UserDto.Response.NecessaryInfo(
                username=user_info['username'],
                age=user_info['age'],
                email=user_info['email'],
                address=user_info['address'],
                detailAddress=user_info['detailAddress']
            )

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