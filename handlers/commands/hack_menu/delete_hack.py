from database import db
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


class Hack_to_delete(StatesGroup):
    option_capture = State()  # если по номеру
    option_confirm = State()


@router.callback_query(F.data == "menu_hack_delete")
async def menu_hack_delete(callback: Message, state: FSMContext):
    hacks = db.get_hacks()
    res = "Выберете хакатон, который нужно убрать:\n"
    for i in range(0, len(hacks)):
        res += f" {i + 1}) {hacks[i][4]}\n"
    await state.set_state(Hack_to_delete.option_capture)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Назад", callback_data="return_to_menu"))
    await callback.message.edit_text(res, reply_markup=builder.as_markup())
    await callback.answer()


@router.message(Hack_to_delete.option_capture, F.text.strip().isdigit())
async def option_capture_number(message: Message, state: FSMContext):
    msg = int(message.text)
    hacks = db.get_hacks()
    if msg - 1 in [x for x in range(0, len(hacks))]:
        res = f"Удалить {hacks[msg - 1][4]}?"
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="Да", callback_data="hack_delete_confirm"),
            InlineKeyboardButton(
                text="Нет", callback_data="hack_delete_abort"),
        )
        await state.update_data(option_capture=hacks[msg - 1][0])
        await state.set_state(Hack_to_delete.option_confirm)
        await message.answer(res, reply_markup=builder.as_markup())
    else:
        await message.answer("Такого хакатона нет, введите корректный номер или имя")


@router.message(Hack_to_delete.option_capture)
async def option_capture_name(message: Message, state: FSMContext):
    msg = message.text
    hacks = db.get_hacks()
    for hack in hacks:
        if hack[4].lower() == msg.lower():
            res = f"Удалить {hack[4]}?"
            builder = InlineKeyboardBuilder()
            builder.row(
                InlineKeyboardButton(
                    text="Да", callback_data="hack_delete_confirm"),
                InlineKeyboardButton(
                    text="Нет", callback_data="hack_delete_abort"),
            )
            await state.update_data(option_capture=hack[0])
            await state.set_state(Hack_to_delete.option_confirm)
            await message.answer(res, reply_markup=builder.as_markup())
            break
    else:
        await message.answer("Такого хакатона нет, введите корректный номер или имя")


@router.callback_query(Hack_to_delete.option_confirm)
async def option_confirm(callback: Message, state: FSMContext):
    command = callback.data.split("_")[2]
    if command == "confirm":
        data = await state.get_data()
        hack = data.get("option_capture")
        db.delete_hack(str(hack))
        await callback.answer("Хакатон удален!")
        await state.clear()
        await menu_hack_delete(callback, state)
    if command == "abort":
        await callback.answer("Все отсалось как и было")
        await state.clear()
        await menu_hack_delete(callback, state)
