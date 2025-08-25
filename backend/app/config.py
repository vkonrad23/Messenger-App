from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    # Default to SQLite for local dev; Docker sets Postgres via .env
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    BACKEND_CORS_ORIGINS: str = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:5173")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "backend/uploads")

settings = Settings()
