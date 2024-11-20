import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def get_session():
    return db.session


class Config:
    mysql_host = os.getenv('MYSQL_HOST') or 'localhost'
    mysql_user = os.getenv('MYSQL_USER') or 'root'
    mysql_password = os.getenv('MYSQL_PASSWORD') or 'root1234'
    mysql_db = os.getenv('MYSQL_DB') or 'perfectfit'

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}'

    if os.getenv("FLASK_ENV") == 'production':
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = False
        SERVER_NAME = os.getenv('PRODUCTION_SERVER_NAME')
    else:
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SQLALCHEMY_ECHO = True
        SERVER_NAME = os.getenv('DEVELOP_SERVER_NAME') or '127.0.0.1:5000'

    SECRET_KEY = os.environ.get('FLASH_SECRET_KEY')
