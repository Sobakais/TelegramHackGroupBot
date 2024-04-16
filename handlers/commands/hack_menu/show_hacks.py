from aiogram import types
from aiogram import F, Router
from aiogram.types import Message
from database.db import get_hacks
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "hack_show_closest")
async def menu_show_closest(call: Message):
    req = get_hacks()
    res = ""
    if req:
        hacks = sorted(req, key=lambda x: (x[2], x[1], x[0]))
        for hack in hacks:
            res += f"{hack[4]} будет {hack[1]}.{hack[2]}.{hack[3]}\n  {hack[5]}\n\n"
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(text="Назад", callback_data="return_to_menu")
        )
    else:
        res = "Ближайшее время хакатонов не намечается"
    await call.message.edit_text(res, reply_markup=builder.as_markup())
    await call.answer("Ближайшие хаки")
