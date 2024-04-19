from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import keyboard.keyboard_menu as kb


router = Router()


async def update(message: Message, text: str, markup: InlineKeyboardBuilder = None):
    await message.edit_text(text, reply_markup=markup)


@router.message(Command("help", prefix="!"))
async def show_help(message: Message, command: CommandObject):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Закрыть", callback_data="close_data"))
    await message.delete()
    await message.answer(
        """
        Доступные комманды:
          !menu - показать меню
          !change_nick <ник> - сменить имя
          !show_nicks - показать все ники в БД
          !get_nick - узнать свой ник
    """,
        reply_markup=builder.as_markup(),
    )


@router.message(Command("menu", prefix="!"))
async def show_menu(message: Message):
    await message.delete()
    await message.answer("Menu", reply_markup=kb.get_menu())


@router.callback_query(F.data.startswith("menu_"))
async def menu_callback(call: Message):
    out = "_".join(call.data.split("_")[1:])
    if out == "hack":
        await update(call.message, "Управление хакатонами", markup=kb.menu_hack())
    if out == "cancel":
        await call.message.delete()
    await call.answer()
