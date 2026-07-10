from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database.db import get_user

from keyboards.user_keyboards import (
    main_keyboard,
    admin_main_keyboard,
    inline_menu_keyboard,
)

from utils.admin import is_admin

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    user_id = message.from_user.id

    keyboard = admin_main_keyboard if is_admin(user_id) else main_keyboard

    await message.answer(
        "Привет! Я твой первый учебный Telegram-бот.\n\n"
        "Снизу появилась обычная reply-клавиатура.",
        reply_markup=keyboard,
    )

    await message.answer(
        "А это inline-меню. Нажми любую кнопку:",
        reply_markup=inline_menu_keyboard,
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
    telegram_user = message.from_user
    db_user = get_user(telegram_user.id)

    if db_user is None:
        await message.answer(
            "Твой профиль:\n\n"
            f"Telegram ID: {telegram_user.id}\n"
            f"Telegram имя: {telegram_user.first_name}\n"
            f"Username: @{telegram_user.username if telegram_user.username else 'не указан'}\n\n"
            "Анкета пока не заполнена.\n"
            "Нажми 📝 Анкета, чтобы заполнить профиль."
        )
        return

    await message.answer(
        "Твой профиль:\n\n"
        f"Telegram ID: {db_user['telegram_id']}\n"
        f"Telegram имя: {db_user['first_name']}\n"
        f"Username: @{db_user['username'] if db_user['username'] else 'не указан'}\n\n"
        "Анкета:\n"
        f"Имя: {db_user['form_name']}\n"
        f"Возраст: {db_user['age']}"
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
        reply_markup=inline_menu_keyboard,
    )

@router.message()
async def echo_message(message: Message):
    await message.answer(f"Я получил сообщение: {message.text}")