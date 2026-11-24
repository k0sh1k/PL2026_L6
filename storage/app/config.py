# Настройки читаются из окружения / .env, значений порта по умолчанию нет
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ST_", env_file=".env")

    host: str
    port: int
    database_url: str
    log_level: str = "INFO"



@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]

