import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): #DeclarativeBase는 SQLAlchemy에서 사용하는 기본 모델 클래스
    pass


db = SQLAlchemy(model_class=Base) #SQLAlchemy 인스턴스 생성


def get_session():
    return db.session


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1234@localhost/perfectfit'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('FLASH_SECRET_KEY')

    # 파일 업로드 폴더 설정
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)