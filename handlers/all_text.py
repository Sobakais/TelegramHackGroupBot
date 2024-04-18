from aiogram import Router, F
from aiogram.types import Message
from database.db import get_user, get_responds
import random

router = Router()


@router.callback_query(F.data == "close_data")
async def close_data(call: Message):
    await call.message.delete()


@router.message()
async def message_with_text(message: Message):
    gen = random.randint(0, 10000)
    user = get_user(message.from_user.id)
    if user and (gen <= user[2] * 100):
        responds = get_responds(message.from_user.id)
        if responds:
            await message.reply(str(random.choice(responds).replace("{name}", user[1])))
