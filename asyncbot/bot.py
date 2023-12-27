from aiogram import Bot, Dispatcher

from .data.settings import secrets

bot: Bot = Bot(token=secrets.BOT_TOKEN, parse_mode="HTML")
dp: Dispatcher = Dispatcher()
