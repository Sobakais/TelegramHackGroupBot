from aiogram import Router, F
from aiogram.types import Message
import random
import resources.config as cfg

router = Router()
router.message.filter(F.from_user.id.in_(cfg.id_users.keys()))


# @router.message()
# async def message_with_text(message: Message):
#     await message.answer(f"Ты ввел: {message.text}")


@router.message(lambda message: message.from_user.id in cfg.go_fuck_your_self)
async def message_with_text(message: Message):
    gen = random.randint(0, 10000)
    if cfg.go_fuck_your_self_chance * 100 >= gen:
        await message.reply(f"Пошел нахуй, {cfg.id_users[message.from_user.id]}!)")
