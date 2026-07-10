from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.profile_states import ProfileForm

from keyboards.user_keyboards import (
    inline_menu_keyboard,
    back_to_menu_keyboard,
    main_keyboard,
    cancel_keyboard,
)

from database.db import get_user

router = Router()


@router.callback_query(F.data == "menu_profile")
async def inline_profile_handler(callback: CallbackQuery):
    telegram_user = callback.from_user
    db_user = get_user(telegram_user.id)

    if db_user is None:
        await callback.message.edit_text(
            "👤 Твой профиль:\n\n"
            f"Telegram ID: {telegram_user.id}\n"
            f"Telegram имя: {telegram_user.first_name}\n"
            f"Username: @{telegram_user.username if telegram_user.username else 'не указан'}\n\n"
            "Анкета пока не заполнена.\n"
            "Нажми 📝 Анкета, чтобы заполнить профиль.",
            reply_markup=back_to_menu_keyboard,
        )

        await callback.answer()
        return

    await callback.message.edit_text(
        "👤 Твой профиль:\n\n"
        f"Telegram ID: {db_user['telegram_id']}\n"
        f"Telegram имя: {db_user['first_name']}\n"
        f"Username: @{db_user['username'] if db_user['username'] else 'не указан'}\n\n"
        "Анкета:\n"
        f"Имя: {db_user['form_name']}\n"
        f"Возраст: {db_user['age']}",
        reply_markup=back_to_menu_keyboard,
    )

    await callback.answer()

@router.callback_query(F.data == "menu_help")
async def inline_help_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ Помощь:\n\n"
        "Это учебный бот.\n"
        "Сейчас мы изучаем inline-кнопки, callback_data и редактирование сообщений.",
        reply_markup=back_to_menu_keyboard,
    )

    await callback.answer()


@router.callback_query(F.data == "menu_catalog")
async def inline_catalog_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "📦 Каталог:\n\n"
        "Пока каталог пуст.\n"
        "Позже здесь можно будет сделать товары, услуги, подписки или заказы.",
        reply_markup=back_to_menu_keyboard,
    )

    await callback.answer("Каталог открыт")


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню.\n\n"
        "Выбери нужный раздел:",
        reply_markup=inline_menu_keyboard,
    )

    await callback.answer()
