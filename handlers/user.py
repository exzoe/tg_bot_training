from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.user_keyboards import (
    main_keyboard,
    inline_menu_keyboard,
)

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "Привет! Я твой первый учебный Telegram-бот.\n\n"
        "Снизу появилась обычная reply-клавиатура.",
        reply_markup=main_keyboard,
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
        reply_markup=inline_menu_keyboard,
    )

@router.message()
async def echo_message(message: Message):
    await message.answer(f"Я получил сообщение: {message.text}")