import re
from database import db
from datetime import datetime
from aiogram import F, Router
from resources.config import state_message
from aiogram.fsm.context import FSMContext
from keyboard import keyboard_menu_hack as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


class Hack_to_edit(StatesGroup):
    option_capture = State()
    hack_edit = State()
    edit_name = State()
    edit_date = State()
    edit_description = State()
    edit_state = State()


@router.callback_query(F.data == "menu_hack_edit")
async def menu_hack_edit(callback: Message, state: FSMContext):
    hacks = db.get_hacks()
    res = "Выберете хакатон, который нужно отредактировать:\n"
    for i in range(0, len(hacks)):
        res += f" {i + 1}) {hacks[i][4]}\n"
    await state.set_state(Hack_to_edit.option_capture)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Назад", callback_data="return_to_menu"))
    await callback.message.edit_text(res, reply_markup=builder.as_markup())
    await callback.answer()


@router.message(Hack_to_edit.option_capture, F.text.strip().isdigit())
async def option_capture_number(message: Message, state: FSMContext):
    msg = int(message.text)
    hacks = db.get_hacks()
    if msg - 1 in [x for x in range(0, len(hacks))]:
        res = f"Редактируем {hacks[msg - 1][6]} {hacks[msg - 1][4]}\nЧто меняем?"
        await state.update_data(option_capture=hacks[msg - 1][0])
        await state.set_state(Hack_to_edit.hack_edit)
        await message.answer(res, reply_markup=kb.hack_edit())
    else:
        await message.answer("Такого хакатона нет, введите корректный номер или имя")


@router.message(Hack_to_edit.option_capture, F.text)
async def option_capture_name(message: Message, state: FSMContext):
    msg = message.text
    hacks = db.get_hacks()
    for hack in hacks:
        if hack[4].lower() == msg.lower():
            res = f"Редактируем {hack[6]} {hack[4]}\nЧто меняем?"
            await state.update_data(option_capture=hack[0])
            await state.set_state(Hack_to_edit.hack_edit)
            await message.answer(res, reply_markup=kb.hack_edit())
            break
    else:
        await message.answer("Такого хакатона нет, введите корректный номер или имя")


@router.callback_query(Hack_to_edit.hack_edit, F.data == "return_to_edit_menu")
async def hack_edit_confirm(callback: Message, state: FSMContext):
    await state.clear()
    await callback.answer()
    await menu_hack_edit(callback, state)


@router.callback_query(Hack_to_edit.hack_edit, F.data.startswith("edit_edit_"))
async def hack_edit(callback: Message, state: FSMContext):
    command = callback.data.split("_")[2]
    if command == "name":
        await state.set_state(Hack_to_edit.edit_name)
        await callback.message.edit_text("Введите название")
    if command == "date":
        await state.set_state(Hack_to_edit.edit_date)
        await callback.message.edit_text("Введите дату")
    if command == "description":
        await state.set_state(Hack_to_edit.edit_description)
        await callback.message.edit_text("Введите описание")
    if command == "state":
        await state.set_state(Hack_to_edit.edit_state)
        await callback.message.edit_text(state_message, reply_markup=kb.state_edit())


@router.callback_query(Hack_to_edit.edit_state, F.data.startswith("state_edit_"))
async def edit_state(callback: Message, state: FSMContext):
    command = callback.data.split("_")[2]
    data = await state.get_data()
    rowid = data.get("option_capture")
    if command == "reg":
        db.set_hack_status(rowid, "✅")
    if command == "unreg":
        db.set_hack_status(rowid, "🚫")
    if command == "work":
        db.set_hack_status(rowid, "💪")
    if command == "unpass":
        db.set_hack_status(rowid, "😐")
    if command == "participants":
        db.set_hack_status(rowid, "🤝")
    if command == "prizes":
        db.set_hack_status(rowid, "🏆")
    await state.clear()
    await state.update_data(option_capture=rowid)
    await state.set_state(Hack_to_edit.hack_edit)
    hack = db.get_hack(rowid)
    await callback.answer()
    await callback.message.edit_text(
        f"Редактируем {hack[6]} {hack[4]}\nЧто меняем?", reply_markup=kb.hack_edit()
    )


@router.message(Hack_to_edit.edit_name)
async def edit_name(message: Message, state: FSMContext):
    data = await state.get_data()
    rowid = data.get("option_capture")
    db.set_hack_name(rowid, message.text)
    await state.clear()
    await state.update_data(option_capture=rowid)
    await state.set_state(Hack_to_edit.hack_edit)
    hack = db.get_hack(rowid)
    await message.answer(
        f"Редактируем {hack[6]} {hack[4]}\nЧто меняем?", reply_markup=kb.hack_edit()
    )


@router.message(Hack_to_edit.edit_date)
async def edit_date(message: Message, state: FSMContext):
    try:
        hdate = list(map(int, re.split(r"\s|/|\.", message.text)))
    except ValueError:
        await message.answer("Введите корректную дату в формате: dd/mm/yyyy")
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
        await message.answer("Введите корректную дату в формате: dd/mm/yyyy")
        return
    data = await state.get_data()
    rowid = data.get("option_capture")
    db.set_hack_date(rowid, hdate)
    await state.clear()
    await state.update_data(option_capture=rowid)
    await state.set_state(Hack_to_edit.hack_edit)
    hack = db.get_hack(rowid)
    await message.answer(
        f"Редактируем {hack[6]} {hack[4]}\nЧто меняем?", reply_markup=kb.hack_edit()
    )


@router.message(Hack_to_edit.edit_description)
async def edit_description(message: Message, state: FSMContext):
    data = await state.get_data()
    rowid = data.get("option_capture")
    db.set_hack_description(rowid, message.text)
    await state.clear()
    await state.update_data(option_capture=rowid)
    await state.set_state(Hack_to_edit.hack_edit)
    hack = db.get_hack(rowid)
    await message.answer(
        f"Редактируем {hack[6]} {hack[4]}\nЧто меняем?", reply_markup=kb.hack_edit()
    )
