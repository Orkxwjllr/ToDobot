import logging
import os
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)

@dataclass
class BotSettings:
    token: str

@dataclass
class LogSettings:
    level: str
    format: str

@dataclass
class dbSettings:
    name: str
    host: str
    port: int
    user: str
    password: str

@dataclass
class RedisSettings:
    db: str
    host: str
    port: int
    user: str
    password: str

@dataclass
class Config:
    bot: BotSettings
    log: LogSettings
    db: dbSettings
    redis: RedisSettings

def load_config(path: str | None = None) -> Config:
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(".env file not found at '%s', skipping...", path)
        else:
            logger.info("Loading .env from '%s'", path)

    env.read_env(path)

    redis = RedisSettings(
        db=env("REDIS_DATABASE"),
        host=env("REDIS_HOST"),
        port=env.int("REDIS_PORT"),
        user=env("REDIS_USERNAME"),
        password=env("REDIS_PASSWORD")
    )

    db = dbSettings(
        name=env("POSTGRES_DB"),
        host=env("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        user=env("POSTGRES_USER"),
        password=env("POSTGRES_PASSWORD"),
    )

    log = LogSettings(
        level=env("LOG_LEVEL"),
        format=env("LOG_FORMAT"),
    )

    bot = BotSettings(
        token=env("BOT_TOKEN")
    )

    logger.info("Configuration loaded successfully")

    return Config(
        bot=bot,
        log=log,
        db=db,
        redis=redis
    )