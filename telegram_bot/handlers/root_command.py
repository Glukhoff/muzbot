from aiogram import types, Dispatcher
from asgiref.sync import async_to_sync
from django.db import IntegrityError

from muzikantoff_admin.models import (
    Person,
    Menu
)
from telegram_bot.callback_menu import callback_menu


async def start_command(message: types.Message):
    try:
        async_to_sync(Person.objects.create(
            chat_id=message.chat.id,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name
        )).awaitable
    except IntegrityError:
        pass

    finally:
        menu = async_to_sync(Menu.objects.filter(parent__isnull=True)).awaitable

    collection_buttons = types.InlineKeyboardMarkup(row_width=2)

    for button in menu:
        if button.url:
            collection_buttons.insert(
                types.InlineKeyboardButton(
                    text=button.title,
                    url=button.url,

                )
            )
            continue

        collection_buttons.insert(
            types.InlineKeyboardButton(
                text=button.title,
                callback_data=callback_menu.new(button_id=button.id))
        )
    await message.answer(text="Приветствуем Вас 🥳\nЭто официальный бот проекта Музыкантофф")
    await message.answer(
        text='Выберите пункт меню:',
        reply_markup=collection_buttons,
        disable_notification=True
    )


def registration_initialization_bot(dp: Dispatcher):
    dp.register_message_handler(start_command, dp.throttled(rate=3), commands=["start"])
