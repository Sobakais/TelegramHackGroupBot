from database import db
from aiogram import F, Router
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
        res = f"Редактируем {hacks[msg - 1][4]}\nЧто меняем?"
        await state.update_data(option_capture=hacks[msg - 1][0])
        await state.set_state(Hack_to_edit.hack_edit)
        await message.answer(res)
    else:
        await message.answer("Такого хакатона нет, введите корректный номер или имя")


@router.message(Hack_to_edit.option_capture)
async def option_capture_name(message: Message, state: FSMContext):
    msg = message.text
    hacks = db.get_hacks()
    for hack in hacks:
        if hack[4].lower() == msg.lower():
            res = f"Редактируем {hack[4]}\nЧто меняем?"
            await state.update_data(option_capture=hack[0])
            await state.set_state(Hack_to_edit.hack_edit)
            await message.answer(res, reply_markup=kb.hack_edit())
            break
    else:
        await message.answer("Такого хакатона нет, введите корректный номер или имя")
