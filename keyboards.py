from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="О нас"), KeyboardButton(text="Меню")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)


inline_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="👤 Профиль",
                callback_data="profile"
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ Помощь",
                callback_data="help"
            )
        ],
        [
            InlineKeyboardButton(
                text="📦 Каталог",
                callback_data="catalog"
            )
        ]
    ]
)