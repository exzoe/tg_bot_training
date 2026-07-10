from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from utils.admin import is_admin
from database.db import count_users
from keyboards.user_keyboards import admin_keyboard


router = Router()

@router.message(Command("admin"))
async def admin_panel_handler(message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.answer("⛔ У тебя нет доступа к админ-панели.")
        return

    await message.answer(
        "Админ-панель:\n\n"
        "Выбери действие:",
        reply_markup=admin_keyboard,
    )


@router.callback_query(F.data == "admin_stats")
async def admin_stats_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    if not is_admin(user_id):
        await callback.answer(
            "Нет доступа",
            show_alert=True,
        )
        return

    users_count = count_users()

    await callback.message.edit_text(
        "📊 Статистика бота:\n\n"
        f"Пользователей в базе: {users_count}",
        reply_markup=admin_keyboard,
    )

    await callback.answer()

@router.message(F.text == "⚙️ Админка")
async def admin_panel_button_handler(message: Message):
    user_id = message.from_user.id

    if not is_admin(user_id):
        await message.answer("⛔ У тебя нет доступа к админ-панели.")
        return

    await message.answer(
        "Админ-панель:\n\n"
        "Выбери действие:",
        reply_markup=admin_keyboard,
    )