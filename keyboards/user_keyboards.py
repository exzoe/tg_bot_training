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

admin_main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Профиль"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="О нас"), KeyboardButton(text="Меню")],
        [KeyboardButton(text="📝 Анкета")],
        [KeyboardButton(text="⚙️ Админка")],
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

profile_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Подтвердить",
                callback_data="profile_confirm",
            )
        ],
        [
            InlineKeyboardButton(
                text="🔁 Заполнить заново",
                callback_data="profile_restart",
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="profile_cancel",
            )
        ],
    ]
)

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📊 Статистика",
                callback_data="admin_stats",
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Пользователи",
                callback_data="admin_users_page:0",
            )
        ],
    ]
)

def get_admin_users_keyboard(
    current_page: int,
    total_pages: int,
) -> InlineKeyboardMarkup:
    buttons = []

    navigation_buttons = []

    if current_page > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"admin_users_page:{current_page - 1}",
            )
        )

    if current_page < total_pages - 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="➡️ Вперед",
                callback_data=f"admin_users_page:{current_page + 1}",
            )
        )

    if navigation_buttons:
        buttons.append(navigation_buttons)

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ В админ-панель",
                callback_data="admin_menu",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)