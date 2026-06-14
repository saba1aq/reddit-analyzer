from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

class BaseConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

class DatabaseSettings(BaseConfigSettings):
    host: Optional[str] = Field(default=None, validation_alias="POSTGRES_HOST")
    port: Optional[int] = Field(default=None, validation_alias="POSTGRES_PORT")
    user: Optional[str] = Field(default=None, validation_alias="POSTGRES_USER")
    password: Optional[str] = Field(default=None, validation_alias="POSTGRES_PASSWORD")
    name: Optional[str] = Field(default=None, validation_alias="POSTGRES_DB")


    @property
    def url(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )

class RedditSettings(BaseConfigSettings):
    email: Optional[str] = Field(default=None, validation_alias="REDDIT_EMAIL")
    password: Optional[str] = Field(default=None, validation_alias="REDDIT_PASSWORD")

class Settings(BaseConfigSettings):
    database: DatabaseSettings = DatabaseSettings()
    reddit: RedditSettings = RedditSettings()


settings = Settings()