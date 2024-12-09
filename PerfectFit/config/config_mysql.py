import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def get_session():
    return db.session()


class Config:
    mariadb_host = os.getenv('MARIADB_HOST') or 'localhost'
    mariadb_port = os.getenv('MARIADB_PORT') or '11401'
    mariadb_user = os.getenv('MARIADB_USERNAME') or 'root'
    mariadb_password = os.getenv('MARIADB_PASSWORD') or '1234'
    mariadb = os.getenv('MARIADB') or 'perfectfit'

    # SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'
    SQLALCHEMY_DATABASE_URI = f'mariadb+pymysql://{mariadb_user}:{mariadb_password}@{mariadb_host}:{mariadb_port}/{mariadb}'


    if os.getenv("FLASK_ENV") == 'production':
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = False
        SERVER_NAME = os.getenv('PRODUCTION_SERVER_NAME')
    else:
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = True
        SERVER_NAME = os.getenv('DEVELOP_SERVER_NAME') or '127.0.0.1:5000' ## 맥북용으로 임시 변경

    SECRET_KEY = os.environ.get('FLASH_SECRET_KEY')