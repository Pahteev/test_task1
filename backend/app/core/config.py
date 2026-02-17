from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "SmartPlant"
    secret_key: str = Field(default="change-me", min_length=16)
    jwt_access_ttl_minutes: int = 15
    jwt_refresh_ttl_days: int = 7
    allowed_origins: list[str] = ["http://localhost:5173"]

    postgres_dsn: str = "postgresql+asyncpg://smartplant:smartplant@db:5432/smartplant"
    redis_dsn: str = "redis://redis:6379/0"
    telegram_token: str = ""
    telegram_encryption_key: str = "change-this-fernet-key"
    ai_service_url: str = "http://ai:8001/classify"


settings = Settings()
