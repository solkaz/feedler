"""
Wrapper to handle environment variables
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Captures settings from a dotenv file
    """

    model_config = SettingsConfigDict(
        env_prefix="FEEDLER_",
        env_file=".env",
        env_file_encoding="utf-8",
    )
    pg_url: str


settings = Settings()
