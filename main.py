import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers.user import router as user_router
from handlers.callbacks import router as callbacks_router
from handlers.profile import router as profile_router
from handlers.admin import router as admin_router

from database.db import init_db

async def main():
    logging.basicConfig(level=logging.INFO)

    init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(profile_router)
    dp.include_router(callbacks_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную")