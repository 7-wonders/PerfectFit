from sqlalchemy import Column, Integer, String, Text, ARRAY
from database.config import Base

class Requirements(Base):
    __tablename__ = 'requirements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    keywords = Column(ARRAY(String), nullable=False)
    job_id = Column(Integer, nullable=False)
    level = Column(String, nullable=False)
    pros = Column(Text, nullable=False)
    cons = Column(Text, nullable=False)
    prompt = Column(Text, nullable=True)  # 선택 필드
    title = Column(ARRAY(String), nullable=True)  # 선택 필드