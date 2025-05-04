from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    ARXIV_TOPIC: str = "machine learning"
    OPENAI_API_KEY: str