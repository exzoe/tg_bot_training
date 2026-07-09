from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="О нас"), KeyboardButton(text="Меню")],
        [KeyboardButton(text="📝 Анкета")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)


inline_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="👤 Профиль",
                callback_data="menu_profile",
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ Помощь",
                callback_data="menu_help",
            )
        ],
        [
            InlineKeyboardButton(
                text="📦 Каталог",
                callback_data="menu_catalog",
            )
        ],
    ]
)


back_to_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅️ Назад в меню",
                callback_data="back_to_menu",
            )
        ]
    ]
)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="❌ Отмена")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Можно отменить действие",
)