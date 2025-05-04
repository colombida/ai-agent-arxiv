from sqlalchemy import create_engine
from database.models import Base
from config.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)