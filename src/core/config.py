from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from src.misc.case_converter import to_camel

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    common: str = "/common"
    call_session: str = "/call_session"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 100
    max_overflow: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisConfig(BaseModel):
    host: str = "redis"
    port: int = 6379
    token_db: int = 1


class UserCredential(BaseModel):
    username: str
    password: str


class CommonConfig(BaseModel):
    chat_count_limit: int = 60 * 60 * 24
    telegram_client_settings_expire: int = 60 * 60 * 24
    days_limit_of_parsing: int = 30
    env: str = "local"
    tg_own_ids: list[int] = [777000]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("..env",),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="allow",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    common: CommonConfig = CommonConfig()
    db: DatabaseConfig
    db_redis: RedisConfig = RedisConfig()
    user_credential: UserCredential
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    version: str = "0.1.0"
    env: str = "local"
    default_timezone: str = "UTC"


settings = Settings()  # type: ignore
