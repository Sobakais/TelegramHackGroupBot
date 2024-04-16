from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def cancel_button():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Назад", callback_data="return_to_menu")
    )
    return builder.as_markup()


def hack_menu_edit():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Дату", callback_data="hack_edit_date"),
        types.InlineKeyboardButton(text="Название", callback_data="hack_edit_name"),
        types.InlineKeyboardButton(
            text="Описание", callback_data="hack_edit_description"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Подтвердить", callback_data="hack_edit_confirm"
        ),
        types.InlineKeyboardButton(text="Назад", callback_data="return_to_menu"),
    )
    return builder.as_markup()
