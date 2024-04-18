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
        types.InlineKeyboardButton(text="Дату", callback_data="hack_menu_edit_date"),
        types.InlineKeyboardButton(
            text="Название", callback_data="hack_menu_edit_name"
        ),
        types.InlineKeyboardButton(
            text="Описание", callback_data="hack_menu_edit_description"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Подтвердить", callback_data="hack_edit_confirm"
        ),
        types.InlineKeyboardButton(text="Назад", callback_data="return_to_menu"),
    )
    return builder.as_markup()


def hack_edit():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Дату", callback_data="edit_edit_date"),
        types.InlineKeyboardButton(text="Название", callback_data="edit_edit_name"),
        types.InlineKeyboardButton(
            text="Описание", callback_data="edit_edit_description"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="Состояние", callback_data="edit_edit_state"),
        types.InlineKeyboardButton(text="Ничего", callback_data="return_to_edit_menu"),
    )
    return builder.as_markup()


def state_edit():
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="1) 🚫", callback_data="state_edit_unreg"),
        types.InlineKeyboardButton(text="2) ✅", callback_data="state_edit_reg"),
        types.InlineKeyboardButton(text="3) 💪", callback_data="state_edit_work"),
    )
    builder.row(
        types.InlineKeyboardButton(text="4) 😐", callback_data="state_edit_unpass"),
        types.InlineKeyboardButton(
            text="5) 🤝", callback_data="state_edit_participants"
        ),
        types.InlineKeyboardButton(text="6) 🏆", callback_data="state_edit_prizes"),
    )
    return builder.as_markup()
