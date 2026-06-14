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

class BrokerSettings(BaseConfigSettings):
    host: str = Field(default="localhost", validation_alias="RABBITMQ_HOST")
    port: int = Field(default=5672, validation_alias="RABBITMQ_PORT")
    user: str = Field(default="guest", validation_alias="RABBITMQ_USER")
    password: str = Field(default="guest", validation_alias="RABBITMQ_PASSWORD")

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}//"


class ScraperSettings(BaseConfigSettings):
    pause_min: float = Field(default=180.0, validation_alias="SCRAPER_PAUSE_MIN")
    pause_max: float = Field(default=300.0, validation_alias="SCRAPER_PAUSE_MAX")
    max_posts: Optional[int] = Field(default=None, validation_alias="SCRAPER_MAX_POSTS")
    proxy: Optional[str] = Field(default=None, validation_alias="SCRAPER_PROXY")


class Settings(BaseConfigSettings):
    database: DatabaseSettings = DatabaseSettings()
    reddit: RedditSettings = RedditSettings()
    broker: BrokerSettings = BrokerSettings()
    scraper: ScraperSettings = ScraperSettings()


settings = Settings()