import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # AI/Grok API key (used in llm_service.py)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "test_key")

    # Database configuration
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "task_breaker")

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
