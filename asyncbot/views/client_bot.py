from typing import Any

from aiohttp import web
from aiojobs.aiohttp import spawn

from asyncbot.bot import bot
from utils import utils

from ..data.settings import secrets
from ..models.methods import SyncCore

routes = web.RouteTableDef()


@routes.post('/pong_send')
async def pong_send(request: web.Request) -> web.Response:
    data: dict[str, Any] = await request.json()
    await bot.send_audio(chat_id=data["user_id"], audio=data["file_id"],
                         caption=data["caption"] + secrets.BOT_USERNAME)
    await utils.delete_message(data["message_user_id"],
                               data["message_bot_id"],
                               chat_id=data["user_id"])
    await spawn(request, SyncCore.add_file(data))
    return web.json_response(status=202)
