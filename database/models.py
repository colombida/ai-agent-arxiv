from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True)
    title = Column(String(500), unique=True)
    abstract = Column(Text)
    url = Column(String(500))
    published = Column(DateTime)