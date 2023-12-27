import logging

import aiojobs.aiohttp
from aiogram import Bot
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiohttp import web

from asyncbot.bot import bot, dp
from asyncbot.data.settings import secrets
from asyncbot.handlers import me_handlers, other_handlers, user_handlers
from asyncbot.views import client_bot
from views import base

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.ERROR,
    filename="asyncbot/data/logs.log"
)

TOKEN = secrets.BOT_TOKEN
WEB_HOST = secrets.WEB_HOST
WEB_PATH = f"/webhook/{TOKEN}"
WEBHOOK_SECRET = secrets.WEBHOOK_SECRET


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{WEB_HOST}{WEB_PATH}", secret_token=WEBHOOK_SECRET)


def main() -> None:
    dp.startup.register(on_startup)

    # registrator router at dispatcher
    dp.include_router(me_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # start webhook and include routes
    app = web.Application()
    app.add_routes(base.routes)
    app.add_routes(client_bot.routes)
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    aiojobs.aiohttp.setup(app)
    webhook_requests_handler.register(app, path=WEB_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host="0.0.0.0", port=8081)


if __name__ == "__main__":
    main()
