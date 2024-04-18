from aiogram import Router
from database.db import init_db, set_chance
from resources.config import admin_tg_id
from database.getAllUsers import get_chat_members
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


@router.message(Command("init_db", prefix="!"))
async def initialize_db(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Закрыть", callback_data="close_data"))
    if message.from_user.id == admin_tg_id and message.chat.type != "private":
        members = await get_chat_members(message.chat.id)
        init_db(members)
        await message.answer("Database initialized!", reply_markup=builder.as_markup())
    else:
        await message.answer(
            "Do not have access to this command", reply_markup=builder.as_markup()
        )
    await message.delete()


@router.message(Command("set_chance", prefix="!"))
async def setchance(message: Message, command: CommandObject):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Закрыть", callback_data="close_data"))
    if command.args is None:
        return
    tgid = message.text.split()[1]
    chance = message.text.split()[2]
    set_chance(tgid, max(0, min(100, int(chance))))
    await message.delete()
