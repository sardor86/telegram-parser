import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from tgbot.config import load_config
from tgbot.handlers import register_all_handlers

from parsers import TMParser, WikkeoParser

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    redis = Redis(host=config.redis.host, port=config.redis.port)

    storage = RedisStorage(redis)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    bot.config = config
    bot.redis = redis

    dp = Dispatcher(storage=storage)
    register_all_handlers(dp)

    bot.parser = dict()
    bot.parser['1688'] = TMParser(bot.config.parsers_api.tm_api)
    bot.parser['wikkeo'] = WikkeoParser()

    for parser in bot.parser:
        bot.parser[parser].get_category()

    # start
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
