from aiogram import types, Dispatcher
from asgiref.sync import async_to_sync

import muzikantoff_admin
from muzikantoff_admin.models import Menu, Post, Stock, Person
from telegram_bot.callback_menu import callback_menu, callback_cancel


async def menu_pagination(callback: types.CallbackQuery, callback_data: dict):
    button_id = callback_data.get("button_id")
    try:
        menu = async_to_sync(Menu.objects.get(id=button_id)).awaitable

    except muzikantoff_admin.models.Menu.DoesNotExist:
        await callback.message.edit_text(
            text="Этого раздела уже нет. 😬 Нажмите /start для обновления списка разделов.")
        return
    submenu = menu.get_children()
    collection_buttons = types.InlineKeyboardMarkup(row_width=2)

    if len(submenu) != 0:
        text_message = f"{menu}"

        for button in submenu:
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
                    callback_data=callback_menu.new(button_id=button.id)
                )
            )
    else:
        try:
            post = async_to_sync(Post.objects.get(menu_id=button_id)).awaitable
            text_message = f"{post.header}\n\n{post.text}"

            if post.is_stock is True:
                collection_buttons.add(
                    types.InlineKeyboardButton(
                        text="Учавствовать",
                        callback_data=callback_cancel.new(button_id=button_id, type="participate")))
            if post.url:
                collection_buttons.insert(
                    types.InlineKeyboardButton(
                        text=post.header,
                        url=post.url,

                    )
                )

        except muzikantoff_admin.models.Post.DoesNotExist:
            text_message = "На данный момент в этом разделе пусто 🙁"

    collection_buttons.add(
        types.InlineKeyboardButton(
            text="⏪ Назад",
            callback_data=callback_cancel.new(button_id=button_id, type="cancel")))

    await callback.message.edit_text(text=text_message, reply_markup=collection_buttons)


async def menu_cancel(callback: types.CallbackQuery, callback_data: dict):
    button_id = callback_data.get("button_id")
    collection_buttons = types.InlineKeyboardMarkup(row_width=2)
    try:
        current_menu = async_to_sync(Menu.objects.get(id=button_id).get_siblings(include_self=True)).awaitable
    except muzikantoff_admin.models.Menu.DoesNotExist:
        await callback.message.edit_text(
            text="Этого раздела уже нет. 😬 Нажмите /start для обновления списка разделов.")
        return

    for button in current_menu:
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
                callback_data=callback_menu.new(button_id=button.id)
            )
        )
    if current_menu.first().get_level() != 0:
        collection_buttons.add(
            types.InlineKeyboardButton(
                text="Назад",
                callback_data=callback_cancel.new(button_id=current_menu.first().parent.id, type="cancel")))

    await callback.message.edit_text(text='Выберите пункт меню:', reply_markup=collection_buttons)


async def stock_participate(callback: types.CallbackQuery, callback_data: dict):
    button_id = callback_data.get("button_id")
    user_id = callback.from_user.id

    try:
        stock_object = async_to_sync(Post.objects.get(menu_id=button_id)).awaitable
        user_object = async_to_sync(Person.objects.get(chat_id=user_id)).awaitable
    except muzikantoff_admin.models.Post.DoesNotExist:
        await callback.message.edit_text(
            text="Этого раздела уже нет. 😬 Нажмите /start для обновления списка разделов.")
        return

    _, result = async_to_sync(Stock.objects.get_or_create(
        first_name=user_object.first_name,
        last_name=user_object.last_name,
        stock_name=stock_object.header,
        stock_id=stock_object.id,
        participant_id=user_object.id
    )).awaitable
    if result is False:
        await callback.answer("Вы уже учавствуете в этом розыгрыше.", show_alert=True)
    await callback.answer(text="Теперь Вы участник. Ожидайте публикации результатов.", show_alert=True)


def register_menu_pagination(dp: Dispatcher):
    dp.register_callback_query_handler(menu_cancel, callback_cancel.filter(type="cancel"), dp.throttled(rate=3))
    dp.register_callback_query_handler(stock_participate, callback_cancel.filter(type="participate"), dp.throttled(rate=3))
    dp.register_callback_query_handler(menu_pagination, callback_menu.filter(), dp.throttled(rate=3))
