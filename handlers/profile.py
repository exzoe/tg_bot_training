from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.user_keyboards import (
    main_keyboard,
    cancel_keyboard,
    profile_confirm_keyboard,
)
from states.profile_states import ProfileForm

from database.db import save_user

router = Router()


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
        "Проверьте данные анкеты:\n\n"
        f"Имя: {data['name']}\n"
        f"Возраст: {data['age']}\n\n"
        "Всё верно?",
        reply_markup=profile_confirm_keyboard,
    )


@router.callback_query(F.data == "profile_confirm")
async def confirm_profile_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user = callback.from_user

    save_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        form_name=data.get("name"),
        age=int(data.get("age")),
    )

    await callback.message.edit_text(
        "✅ Анкета сохранена:\n\n"
        f"Имя: {data.get('name')}\n"
        f"Возраст: {data.get('age')}"
    )

    await state.clear()

    await callback.message.answer(
        "Возвращаю главное меню.",
        reply_markup=main_keyboard,
    )

    await callback.answer("Анкета сохранена")


@router.callback_query(F.data == "profile_restart")
async def restart_profile_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(ProfileForm.name)

    await callback.message.delete()

    await callback.message.answer(
        "Заполняем анкету заново.\n\n"
        "Введите ваше имя:",
        reply_markup=cancel_keyboard,
    )

    await callback.answer()


@router.callback_query(F.data == "profile_cancel")
async def cancel_profile_callback_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.edit_text(
        "❌ Заполнение анкеты отменено."
    )

    await callback.message.answer(
        "Возвращаю главное меню.",
        reply_markup=main_keyboard,
    )

    await callback.answer("Отменено")