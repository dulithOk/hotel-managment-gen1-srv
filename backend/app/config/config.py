from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings

# Load .env from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        # Allow reading from .env automatically if exists
        env_file = env_path
        env_file_encoding = "utf-8"

settings = Settings()
