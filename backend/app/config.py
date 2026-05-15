from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+asyncpg://thrifty:thrifty@localhost:5432/thrifty"
    session_secret: str = "change-me-for-local-development-only"
    smtp_host: str = "smtp.postmarkapp.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    smtp_from: str = "alerts@thrifty.app"
    app_base_url: str = "https://thrifty.app"
    apns_key_id: str = ""
    apns_team_id: str = ""
    apns_key_path: str = "/secrets/apns.p8"
    apns_bundle_id: str = "app.thrifty.ios"
    fcm_credentials_path: str = "/secrets/fcm.json"
    sentry_dsn: str = ""
    log_level: str = Field(default="INFO")


@lru_cache
def get_settings() -> Settings:
    return Settings()
