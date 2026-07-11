from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from utils.admin import is_admin
from database.db import count_users, get_users
from keyboards.user_keyboards import admin_keyboard, get_admin_users_keyboard


router = Router()
USERS_PER_PAGE = 5

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

@router.callback_query(F.data == "admin_menu")
async def admin_menu_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    if not is_admin(user_id):
        await callback.answer(
            "Нет доступа",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "Админ-панель:\n\n"
        "Выбери действие:",
        reply_markup=admin_keyboard,
    )

    await callback.answer()

@router.callback_query(lambda callback: callback.data and callback.data.startswith("admin_users_page:"))
async def admin_users_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    if not is_admin(user_id):
        await callback.answer(
            "Нет доступа",
            show_alert=True,
        )
        return

    page = int(callback.data.split(":")[1])

    total_users = count_users()
    total_pages = max(1, (total_users + USERS_PER_PAGE - 1) // USERS_PER_PAGE)

    if page < 0:
        page = 0

    if page > total_pages - 1:
        page = total_pages - 1

    offset = page * USERS_PER_PAGE

    users = get_users(
        limit=USERS_PER_PAGE,
        offset=offset,
    )

    if not users:
        await callback.message.edit_text(
            "👥 Пользователи\n\n"
            "В базе пока нет пользователей.",
            reply_markup=get_admin_users_keyboard(
                current_page=page,
                total_pages=total_pages,
            ),
        )

        await callback.answer()
        return

    text_lines = [
        "👥 Пользователи",
        "",
        f"Страница: {page + 1}/{total_pages}",
        f"Всего пользователей: {total_users}",
        "",
    ]

    for index, user in enumerate(users, start=offset + 1):
        username = f"@{user['username']}" if user["username"] else "не указан"
        first_name = user["first_name"] if user["first_name"] else "не указано"
        form_name = user["form_name"] if user["form_name"] else "не заполнено"
        age = user["age"] if user["age"] else "не заполнен"

        text_lines.append(
            f"{index}. {form_name}\n"
            f"   Telegram ID: {user['telegram_id']}\n"
            f"   Telegram имя: {first_name}\n"
            f"   Username: {username}\n"
            f"   Возраст: {age}\n"
        )

    await callback.message.edit_text(
        "\n".join(text_lines),
        reply_markup=get_admin_users_keyboard(
            current_page=page,
            total_pages=total_pages,
        ),
    )

    await callback.answer()