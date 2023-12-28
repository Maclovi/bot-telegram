import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from utils import utils

from ..data.settings import UserValidate, secrets
from ..exservies import request
from ..keyboards import set_menu
from ..lexicon.lexicon import LEXICON_RU
from ..models.methods import SyncCore
from ..services.services import get_random_response

# register logger
logger = logging.getLogger(__name__)

# init router level of module
router = Router()
router.message.filter(F.chat.type == "private")


@router.message(CommandStart())
async def proccess_cmd_start(message: Message) -> None:
    assert message.from_user is not None

    text: str = (
        f"Привет, <b>{message.from_user.first_name}</b>🤚"
        f"\n\n{LEXICON_RU['/start']}"
    )
    bot_answer = await message.answer(text, reply_markup=set_menu.keyboard)
    # write to data base
    is_new_user: bool = SyncCore.add_person(UserValidate(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
        status='active',
    ))
    if not is_new_user:
        await utils.sleep_and_delete(message, bot_answer, timer=10)


@router.message(F.text == "Помощь🚒")
async def send_info(message: Message) -> None:
    bot_answer: Message = await message.answer(LEXICON_RU["/start"])
    await utils.sleep_and_delete(message, bot_answer, timer=30)


@router.message(F.text == "Легально?⚠")
async def send_about_legal(message: Message) -> None:
    bot_answer: Message = await message.answer(LEXICON_RU["Легально?⚠"])
    await utils.sleep_and_delete(message, bot_answer, timer=15)


@router.message(F.text == "Свой бот🤖")
async def send_info_own(message: Message) -> None:
    bot_answer: Message = await message.answer(LEXICON_RU["Свой бот🤖"])
    await utils.sleep_and_delete(message, bot_answer, timer=10)


@router.message(F.text == "Предсказания🎱")
async def send_prediction(message: Message) -> None:
    bot_message: str = get_random_response(LEXICON_RU["Шар предсказания🎱"])
    bot_answer: Message = await message.answer(bot_message)
    await utils.sleep_and_delete(message, bot_answer, timer=10)


@router.message(F.text == "Ответ на вопрос🎱")
async def send_ball_response(message: Message) -> None:
    bot_message: str = get_random_response(LEXICON_RU["Ответ на вопрос🎱"])
    bot_answer: Message = await message.answer(bot_message)
    await utils.sleep_and_delete(message, bot_answer, timer=10)


@router.message(lambda message: "youtu" in message.text)
async def send_youtube_music(message: Message) -> None:
    assert message.from_user is not None
    assert message.text is not None

    bot_answer: Message = await message.answer("<em><b>Проверяю..</b></em>")
    file_data = SyncCore.get_file(message.text, message.from_user.id)
    if file_data:
        await message.answer_audio(file_data[0],
                                   caption=file_data[1] + secrets.BOT_USERNAME)
        await utils.sleep_and_delete(message, bot_answer)
        return

    response: str = await request.ping_message(dict(
        url=message.text,
        user_id=message.from_user.id,
        message_user_id=message.message_id,
        message_bot_id=bot_answer.message_id,
    ))
    text: str = (
        f"<em><b>Примерное время ожидания ~ {response}мин.</b></em>"
        if response else
        "<b>Что-то пошло не так, повторите попытку позже..</b>"
    )
    await bot_answer.edit_text(text)
