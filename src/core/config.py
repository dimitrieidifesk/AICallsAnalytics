from datetime import date
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel, ConfigDict, HttpUrl
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from src.misc.case_converter import to_camel

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
logger.add(
    f"{BASE_DIR.parent}/logs/{date.today()}.log",
    colorize=True,
    format="[{level}] | {time:YYYY-MM-DD at HH:mm:ss} | {message}",
    level="INFO"
)

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


class RabbitConfig(BaseModel):
    host: str
    port: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


class UserCredentialConfig(BaseModel):
    username: str
    password: str


class OpenAiConfig(BaseModel):
    api_key: str
    base_url: HttpUrl
    transcription_path: str
    chat_path: str
    whisper_model: str
    chat_model: str
    proxy_url: HttpUrl
    language_code: str = "ru"

    @property
    def audio_transcription_url(self) -> str:
        return str(self.base_url).strip("/") + self.transcription_path

    @property
    def chat_gpt_url(self) -> str:
        return str(self.base_url).strip("/") + self.chat_path


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
    db: DatabaseConfig
    user_credential: UserCredentialConfig
    open_ai: OpenAiConfig
    rabbit: RabbitConfig
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    version: str = "0.1.0"
    env: str
    domain: str
    number_of_processes: int
    default_timezone: str = "UTC"


settings = Settings()  # type: ignore
