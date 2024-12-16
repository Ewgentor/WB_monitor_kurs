import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from aiogram.client.session.aiohttp import AiohttpSession

from config.config import load_config
from database.db import on_startup
from handlers import user_handlers
from windows.windows import get_main_dialog, get_product_dialog, get_bookmarks_dialog
from aiogram.fsm.storage.memory import MemoryStorage


async def main():
    session = AiohttpSession(proxy="http://proxy.server:3128")
    storage = MemoryStorage()
    config = load_config()
    bot = Bot(
        token=config.tg_bot.token,
        # session=session
    )
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        user_handlers.router,
        get_main_dialog(),
        get_product_dialog(),
        get_bookmarks_dialog()
    )
    setup_dialogs(dp)
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Бот запущен")
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    asyncio.run(main())
