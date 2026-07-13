from pydantic_settings import BaseSettings, SettingsConfigDict


# Попробовать сделать с помощью python-dotenv / pydantic-settings
from dataclasses import dataclass, field


class Settings(BaseSettings):
    DATABASE_URL: str
    CORS_ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
    )


settings = Settings()


def get_settings() -> Settings:
    return settings


# Ниже - прямая передача данных в класс Settings

# @dataclass(frozen=True) # Защита от дурака
# class Settings:
#     DATABASE_URL: str = "postgresql+psycopg://postgres:<your_password>@127.0.0.1:5432/postgres"
#     CORS_ALLOWED_ORIGINS: list[str] = field(default_factory=lambda:
#     ["http://localhost:3000"]
# )


# def get_settings() -> Settings:
#     return Settings(
#         DATABASE_URL = "postgresql+psycopg://postgres:<your_password>@127.0.0.1:5432/postgres",
#         CORS_ALLOWED_ORIGINS = ["http://localhost:3000"],
#     )