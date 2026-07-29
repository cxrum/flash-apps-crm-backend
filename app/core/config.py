from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(alias="APP_NAME")
    api_host: str = Field(alias="API_HOST")
    api_port: int = Field(alias="API_PORT")

    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")

    redis_host: str = Field(alias="REDIS_HOST")
    redis_port: str = Field(alias="REDIS_PORT")
    redis_idempotency_key_ttl_seconds: int = Field(alias="REDIS_IDEMPOTENCY_KEY_TTL_SECONDS", default=43200)

    app_secret: str = Field(alias="APP_SECRET")
    batch_rate_limit_per_window: int = Field(default=120, alias="BATCH_RATE_LIMIT_PER_MINUTE")
    rate_limit_window_seconds: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    debug_mode: bool = Field(default=False, alias="DEBUG_MODE")

    ip2location_bin_database_path: str = Field(alias="IP2LOCATION_BIN_DATABASE_PATH")

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            "postgresql+psycopg2://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_uri(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"


settings = Settings()  # type: ignore
