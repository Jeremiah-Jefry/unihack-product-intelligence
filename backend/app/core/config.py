"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings — loaded from environment variables or .env file."""

    # Application
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./data/storage/product_intelligence.db"

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_ORG_ID: str = ""

    # Frontend
    FRONTEND_URL: str = "http://localhost:8501"

    # Storage
    UPLOAD_DIR: str = "./data/uploads"
    STORAGE_DIR: str = "./data/storage"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
