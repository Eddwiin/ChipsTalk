"""Application configuration.

All configuration comes from environment variables (optionally loaded from
a local `.env` file for development). Nothing here should ever contain a
real secret: `.env` is git-ignored and `.env.example` only holds placeholders.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    environment: str = "development"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "chipstalk"
    postgres_password: str = "changeme"
    postgres_db: str = "chipstalk"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (env vars are read once per process)."""
    return Settings()
