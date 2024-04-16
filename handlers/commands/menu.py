from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
import keyboard.keyboard_menu as kb


router = Router()


async def update(message: Message, text: str, markup: InlineKeyboardBuilder = None):
    await message.edit_text(text, reply_markup=markup)


@router.message(Command("help", prefix="!"))
async def show_help(message: Message, command: CommandObject):
    await message.answer("""
        Доступные комманды:
          !menu - показать меню
          !change_nick <ник> - сменить имя
          !show_nicks - показать все ники в БД
          !get_nick - узнать свой ник
    """)


@router.message(Command("menu", prefix="!"))
async def show_menu(message: Message):
    await message.answer("Menu", reply_markup=kb.get_menu())


@router.callback_query(F.data.startswith("menu_"))
async def menu_callback(call: Message):
    out = "_".join(call.data.split("_")[1:])
    if out == "hack":
        await update(call.message, "------------------", markup=kb.menu_hack())
    if out == "hack_closest":
        await update(call.message, "Хаки (ближайшее)", markup=kb.menu_hack_closest())
    if out == "cancel":
        await call.message.delete()
    await call.answer()
