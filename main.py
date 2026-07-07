import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards import main_keyboard, inline_menu_keyboard


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "Привет! Я твой первый учебный Telegram-бот.\n\n"
        "Снизу появилась обычная reply-клавиатура.",
        reply_markup=main_keyboard
    )

    await message.answer(
        "А это inline-меню. Нажми любую кнопку:",
        reply_markup=inline_menu_keyboard
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Я пока умею:\n\n"
        "/start - запустить бота\n"
        "/help - показать помощь\n\n"
        "Также у меня есть reply-кнопки и inline-кнопки."
    )


@router.message(F.text == "Профиль")
async def profile_handler(message: Message):
    user = message.from_user

    await message.answer(
        f"Твой профиль:\n\n"
        f"ID: {user.id}\n"
        f"Имя: {user.first_name}\n"
        f"Username: @{user.username if user.username else 'не указан'}"
    )


@router.message(F.text == "Помощь")
async def help_button_handler(message: Message):
    await message.answer(
        "Это раздел помощи.\n\n"
        "Пока бот учебный, но позже мы добавим больше функций."
    )


@router.message(F.text == "О нас")
async def about_handler(message: Message):
    await message.answer(
        "Это учебный бот для тренировки разработки Telegram-ботов на aiogram."
    )


@router.message(F.text == "Меню")
async def menu_handler(message: Message):
    await message.answer(
        "Открываю inline-меню:",
        reply_markup=inline_menu_keyboard
    )


@router.callback_query(F.data == "profile")
async def inline_profile_handler(callback: CallbackQuery):
    user = callback.from_user

    await callback.message.answer(
        f"Inline-профиль:\n\n"
        f"ID: {user.id}\n"
        f"Имя: {user.first_name}\n"
        f"Username: @{user.username if user.username else 'не указан'}"
    )

    await callback.answer()


@router.callback_query(F.data == "help")
async def inline_help_handler(callback: CallbackQuery):
    await callback.message.answer(
        "Inline-помощь:\n\n"
        "Ты нажал inline-кнопку, а не отправил обычное сообщение."
    )

    await callback.answer()


@router.callback_query(F.data == "catalog")
async def inline_catalog_handler(callback: CallbackQuery):
    await callback.message.answer(
        "Каталог пока пуст.\n\n"
        "Позже тут могут быть товары, услуги, подписки или заказы."
    )

    await callback.answer("Каталог открыт")


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