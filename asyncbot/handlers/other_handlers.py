from aiogram import F, Router
from aiogram.filters import KICKED, MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message

from ..models.methods import SyncCore
from ..data.settings import UserValidate

# init router a level of module
router = Router()
router.message.filter(F.chat.type == "private")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated) -> None:
    SyncCore.update_person(UserValidate(
        user_id=event.from_user.id,
        first_name=event.from_user.first_name,
        last_name=event.from_user.last_name,
        username=event.from_user.username,
        status='inactive',
    ))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def process_user_unblocked_bot(event: ChatMemberUpdated) -> None:
    SyncCore.update_person(UserValidate(
        user_id=event.from_user.id,
        first_name=event.from_user.first_name,
        last_name=event.from_user.last_name,
        username=event.from_user.username,
        status='active',
    ))


@router.message()
async def send_echo(message: Message) -> None:
    await message.answer("Мне не удалось вас понять :(")
