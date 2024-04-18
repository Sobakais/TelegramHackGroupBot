from database import db
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command("change_nick", prefix="!"))
async def change_nick(message: Message, command: CommandObject):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Закрыть", callback_data="close_data"))
    if command.args is None:
        await message.answer("Формат команды !change_nick <ник>")
        return
    nick = message.text.split()[1]
    db.chng_nick(message.from_user.id, nick)
    await message.delete()
    await message.answer(
        f"Никнейм обновлен на {nick}", reply_markup=builder.as_markup()
    )


@router.message(Command("get_nick", prefix="!"))
async def get_nick(message: Message):
    await message.delete()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Закрыть", callback_data="close_data"))
    await message.answer(
        db.get_nick(message.from_user.id), reply_markup=builder.as_markup()
    )


@router.message(Command("show_nicks", prefix="!"))
async def show_nicks(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Закрыть", callback_data="close_data"))
    await message.delete()
    await message.answer(db.show_all(), reply_markup=builder.as_markup())
