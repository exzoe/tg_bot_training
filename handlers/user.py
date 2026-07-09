from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.profile_states import ProfileForm

from keyboards.user_keyboards import main_keyboard, inline_menu_keyboard, cancel_keyboard

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

@router.message(StateFilter("*"), Command("cancel"))
@router.message(StateFilter("*"), F.text == "❌ Отмена")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer(
            "Сейчас нечего отменять.",
            reply_markup=main_keyboard,
        )
        return

    await state.clear()

    await message.answer(
        "Действие отменено. Возвращаю главное меню.",
        reply_markup=main_keyboard,
    )

@router.message(F.text == "📝 Анкета")
async def start_profile_form(message: Message, state: FSMContext):
    await state.set_state(ProfileForm.name)

    await message.answer(
        "Начинаем заполнение анкеты.\n\n"
        "Введите ваше имя:",
        reply_markup=cancel_keyboard,
    )


@router.message(ProfileForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await state.set_state(ProfileForm.age)

    await message.answer(
        "Имя сохранено.\n\n"
        "Теперь введите ваш возраст:"
    )


@router.message(ProfileForm.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте еще раз:")
        return

    await state.update_data(age=message.text)

    data = await state.get_data()

    await message.answer(
        "Анкета заполнена:\n\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}",
        reply_markup=main_keyboard,
    )

    await state.clear()


@router.message()
async def echo_message(message: Message):
    await message.answer(f"Я получил сообщение: {message.text}")