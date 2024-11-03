# импорты
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers import hello, main_catcher
from texts import bot2

logging.basicConfig(level=logging.INFO)


async def main():
    dp = Dispatcher()
    dp.include_routers(hello.router, main_catcher.router)
    await bot2.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot2)


if __name__ == "__main__":
    asyncio.run(main())
