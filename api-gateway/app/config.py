# Адрес соседнего сервиса и таймаут читаются из окружения / .env
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GW_", env_file=".env")

    host: str
    port: int
    storage_base_url: str
    storage_timeout_s: float
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]