from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Подтвердить", callback_data="nickname_confirm"
        ),
        types.InlineKeyboardButton(text="Отмена", callback_data="nickname_cancel"),
    )
    return builder.as_markup()
