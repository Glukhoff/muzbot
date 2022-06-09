import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from telegram_bot.handlers.menu import register_menu_pagination
from telegram_bot.handlers.root_command import registration_initialization_bot


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт бота"),
    ]
    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=os.environ.get('BOT_TOKEN', default=None), parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    registration_initialization_bot(dp)
    register_menu_pagination(dp)

    await set_commands(bot)

    try:
        await dp.start_polling()

    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
