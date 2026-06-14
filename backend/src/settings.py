from typing import Optional
from pydantic import Field
from pydantic_settings import (
    BaseSettings, 
    SettingsConfigDict
)


class BaseConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

class DatabaseSettings(BaseConfigSettings):
    host: Optional[str] = Field(default=None, validation_alias="DB_HOST")
    port: Optional[int] = Field(default=None, validation_alias="DB_PORT")
    user: Optional[str] = Field(default=None, validation_alias="DB_USER")
    password: Optional[str] = Field(default=None, validation_alias="DB_PASSWORD")
    name: Optional[str] = Field(default=None, validation_alias="DB_NAME")


    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

class RedditSettings(BaseConfigSettings):
    email: Optional[str] = Field(default=None, validation_alias="REDDIT_EMAIL")
    password: Optional[str] = Field(default=None, validation_alias="REDDIT_PASSWORD")

class Settings(BaseConfigSettings):
    reddit: RedditSettings = RedditSettings()


settings = Settings()