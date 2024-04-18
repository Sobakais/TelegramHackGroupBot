from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Управление хакатонами", callback_data="menu_hack"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Ближайшие хакатоны", callback_data="menu_hack_closest"
        ),
    )
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="menu_cancel"))
    return builder.as_markup()


def menu_hack():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="Добавить хакатон", callback_data="menu_hack_add"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Редактировать хакатон", callback_data="menu_hack_edit"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Удалить хакатон", callback_data="menu_hack_delete"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="Назад", callback_data="return_to_menu")
    )
    return builder.as_markup()


def menu_hack_closest():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Показать ближайшие", callback_data="hack_show_closest"
        )
    )
    builder.row(
        types.InlineKeyboardButton(text="Назад", callback_data="return_to_menu")
    )
    return builder.as_markup()
