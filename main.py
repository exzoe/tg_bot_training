import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards import main_keyboard


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "Привет! Я твой первый учебный Telegram-бот.\n\n"
        "Выбери действие с помощью кнопок ниже.",
        reply_markup=main_keyboard
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Я пока умею немного:\n\n"
        "/start - запустить бота\n"
        "/help - показать помощь\n\n"
        "А еще у меня есть кнопки меню."
    )


@router.message(lambda message: message.text == "Профиль")
async def profile_handler(message: Message):
    user = message.from_user
    await message.answer(
        f"Твой профиль:\n\n"
        f"ID: {user.id}\n"
        f"Имя: {user.first_name}\n"
        f"Username: @{user.username if user.username else 'не указан'}"
    )


@router.message(lambda message: message.text == "Помощь")
async def help_button_handler(message: Message):
    await message.answer(
        "Это раздел помощи.\n\n"
        "Пока бот учебный, но позже мы добавим больше функций."
    )


@router.message(lambda message: message.text == "О нас")
async def about_handler(message: Message):
    await message.answer(
        "Это учебный бот для тренировки разработки Telegram-ботов на aiogram."
    )


@router.message()
async def echo_message(message: Message):
    await message.answer(f"Я получил сообщение: {message.text}")


async def main():
    logging.basicConfig(level=logging.INFO)

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден. Проверь файл .env")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен вручную")