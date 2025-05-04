from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    arxiv_api_key: str = Field(..., env="ARXIV_API_KEY")
    database_url: str = Field(..., env="DATABASE_URL")
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    class Config:
        env_file = ".env"

settings = Settings()