from database import db
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

router = Router()


@router.message(Command("change_nick", prefix="!"))
async def cmd_settimer(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("Формат команды !change_nick <ник>")
        return
    nick = message.text.split()[1]
    db.chng_nick(message.from_user.id, nick)
    await message.answer(f"Никнейм обновлен на {nick}")
    await message.delete()


@router.message(Command("get_nick", prefix="!"))
async def get_nick(message: Message):
    await message.answer(db.get_nick(message.from_user.id))


@router.message(Command("show_nicks", prefix="!"))
async def show_nicks(message: Message):
    await message.answer(db.show_all())
