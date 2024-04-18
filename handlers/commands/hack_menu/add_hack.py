import re
from typing import Any, Dict
from aiogram import F, Router
from datetime import datetime
from database.db import add_hack
from aiogram.types import Message
from keyboard import keyboard_menu as kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboard.keyboard_menu_hack import cancel_button, hack_menu_edit


router = Router()


class Hack_info(StatesGroup):
    date = State()
    name = State()
    description = State()
    re_date = State()
    re_name = State()
    to_confirm = State()


async def update(message: Message, text: str, markup: InlineKeyboardBuilder = None):
    await message.edit_text(text, reply_markup=markup)


async def hack_reassure(message: Message, data: Dict[str, Any]) -> None:
    date = data.get("date")
    name = data.get("name")
    description = data.get("description")
    text = f"Хакатон {name} будет {date[:-5]}!\n{description} \nВсе верно?\nМожно отредактировать:"
    await message.answer(text=text, reply_markup=hack_menu_edit())


@router.callback_query(F.data == "return_to_menu")
async def return_to_menu(call: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await update(call.message, "Menu", markup=kb.get_menu())
        return

    await state.clear()
    await update(call.message, "Menu", markup=kb.get_menu())


@router.callback_query(F.data.startswith("hack_edit_"))
async def hack_edit_change_handler(callback: Message, state: FSMContext) -> None:
    command = callback.data.split("_")[-1]
    if command == "date":
        await state.set_state(Hack_info.re_date)
        await callback.message.answer(
            "Когда начало хакатона?", reply_markup=cancel_button()
        )
        await callback.answer()
    elif command == "name":
        await state.set_state(Hack_info.re_name)
        await callback.message.answer(
            "Как называется хакатон?", reply_markup=cancel_button()
        )
        await callback.answer()
    elif command == "description":
        await state.set_state(Hack_info.description)
        await callback.message.answer(
            "Введите новое описание",
            reply_markup=cancel_button(),
        )
        await callback.answer()
    elif command == "confirm":
        data = await state.get_data()
        date = re.split(r"\s|/|\.", data.get("date"))
        name = data.get("name")
        description = data.get("description")
        add_hack(date, name, description)
        await update(callback.message, "Menu", markup=kb.get_menu())
        await callback.answer("Хакатон успешно добавлен")


@router.callback_query(F.data == "hack_edit_confirm")
async def hack_edit_confirm(callback: Message, state: FSMContext) -> None:
    await state.clear()
    await update(callback.message, "Menu", markup=kb.get_menu())
    await state.clear()
    await callback.answer("Хакатон успешно добавлен")


@router.callback_query(F.data == "menu_hack_add")
async def menu_hack_add(callback: Message, state: FSMContext) -> None:
    await state.set_state(Hack_info.date)
    await callback.message.answer(
        "Когда начало хакатона?", reply_markup=cancel_button()
    )
    await callback.answer()


@router.message(Hack_info.date)
async def hack_date_capture(message: Message, state: FSMContext) -> None:
    try:
        hdate = list(map(int, re.split(r"\s|/|\.", message.text)))
    except ValueError:
        await message.answer(
            "Введите корректную дату в формате: dd/mm/yyyy",
            reply_markup=cancel_button(),
        )
        return

    now = datetime.now()
    if (
        len(hdate) != 3
        or (hdate[0] < now.day and hdate[1] == now.month and hdate[2] == now.year)
        or hdate[0] > 31
        or (hdate[1] < now.month and hdate[2] == now.year)
        or hdate[1] > 12
        or hdate[2] < now.year
    ):
        await message.answer(
            "Введите корректную дату в формате: dd/mm/yyyy",
            reply_markup=cancel_button(),
        )
        return
    await state.update_data(date=message.text.strip())
    await state.set_state(Hack_info.name)
    await message.answer("Как называется хакатон?", reply_markup=cancel_button())


@router.message(Hack_info.re_date)
async def hack_re_date_capture(message: Message, state: FSMContext) -> None:
    try:
        hdate = list(map(int, re.split(r"\s|/|\.", message.text)))
    except ValueError:
        await message.answer(
            "Введите корректную дату в формате: dd/mm/yyyy",
            reply_markup=cancel_button(),
        )
        return

    now = datetime.now()
    if (
        len(hdate) != 3
        or (hdate[0] < now.day and hdate[1] == now.month and hdate[2] == now.year)
        or hdate[0] > 31
        or (hdate[1] < now.month and hdate[2] == now.year)
        or hdate[1] > 12
        or hdate[2] < now.year
    ):
        await message.answer(
            "Введите корректную дату в формате: dd/mm/yyyy",
            reply_markup=cancel_button(),
        )
        return
    data = await state.update_data(date=message.text.strip())
    await state.set_state(Hack_info.to_confirm)
    await hack_reassure(message, data)


@router.message(Hack_info.name)
async def hack_name_capture(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text.strip())
    await state.set_state(Hack_info.description)
    await message.answer(
        "Тут можно указать краткое описание (к примеру ссылки на регистрацию, конкретный кейс etc.)",
        reply_markup=cancel_button(),
    )


@router.message(Hack_info.re_name)
async def hack_re_name_capture(message: Message, state: FSMContext) -> None:
    data = await state.update_data(name=message.text.strip())
    await state.set_state(Hack_info.to_confirm)
    await hack_reassure(message, data)


@router.message(Hack_info.description)
async def hack_description_capture(message: Message, state: FSMContext) -> None:
    data = await state.update_data(description=message.text)
    await hack_reassure(message, data)
    await state.set_state(Hack_info.to_confirm)
