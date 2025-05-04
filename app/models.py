from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Paper(Base):
    __tablename__ = 'papers'
    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    abstract = Column(Text)
    vector = Column(Text)  # store embedding as JSON list