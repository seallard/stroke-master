"""Application settings, loaded from environment (and an optional .env file)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Core
    database_url: str = "postgresql://stroke:stroke@localhost:5432/stroke"
    redis_url: str = "redis://localhost:6379/0"
    app_base_url: str = "http://localhost:8000"
    secret_key: str = "dev-secret-change-me"

    # Strava OAuth app
    strava_client_id: str = ""
    strava_client_secret: str = ""
    strava_webhook_verify_token: str = "dev-verify-token"

    # Object storage (S3-compatible) for raw streams
    s3_endpoint: str = ""
    s3_bucket: str = "stroke-streams"
    s3_access_key_id: str = ""
    s3_secret_access_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
