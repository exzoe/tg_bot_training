from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.user_keyboards import inline_menu_keyboard, back_to_menu_keyboard


router = Router()


@router.callback_query(F.data == "menu_profile")
async def inline_profile_handler(callback: CallbackQuery):
    user = callback.from_user

    await callback.message.edit_text(
        f"👤 Твой профиль:\n\n"
        f"ID: {user.id}\n"
        f"Имя: {user.first_name}\n"
        f"Фамилия: {user.last_name if user.last_name else 'не указана'}\n"
        f"Username: @{user.username if user.username else 'не указан'}",
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