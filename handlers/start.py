from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.getAllUsers import get_chat_members
from database.db import init_db


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    members = await get_chat_members(message.chat.id)
    init_db(members)
    await message.answer("I'm working!")
