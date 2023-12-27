from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from ..data.settings import secrets

router = Router()
router.message.filter(F.from_user.id == secrets.ME_ID)


@router.message(Command("log"))
async def hello_boss(message: Message) -> None:
    await message.answer("Hi boss")
