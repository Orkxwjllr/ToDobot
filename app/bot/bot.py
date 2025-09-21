import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from app.bot.handlers.user import user_router
from config.config import Config
from app.infrastructure.connection.connection import get_session
from app.bot.middlewares.database import DBSessionMiddleware
from redis.asyncio import Redis



logger = logging.getLogger(__name__)

async def main(config: Config) -> None:
    logger.info("Starting bot...")

    storage = RedisStorage(
        redis=Redis(
            db=config.redis.db,
            host=config.redis.host,
            port=config.redis.port,
            username=config.redis.user,
            password=config.redis.password,
        )
    )

    bot = Bot(
            token=config.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
    dp = Dispatcher(storage=storage)

    db_session = get_session(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password
    )

    logger.info("Including routers...")
    dp.include_router(user_router)

    logger.info("Including middlewares...")
    dp.update.middleware(DBSessionMiddleware())

    try:
        await dp.start_polling(
            bot, db_session= db_session
        )
    except Exception as e:
        logger.exception(e)
    finally:
        db_session.close()
        logger.info("Connection to Postgres closed")
