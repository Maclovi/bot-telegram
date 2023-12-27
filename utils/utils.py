import asyncio

from aiogram.types import Message

from asyncbot.bot import bot


async def sleep_and_delete(*messages: Message, timer: float = 0) -> None:
    await asyncio.sleep(timer)
    for message in messages:
        await message.delete()


async def delete_message(*messages_id: int, chat_id: int) -> None:
    for message in messages_id:
        await bot.delete_message(chat_id=chat_id, message_id=message)
