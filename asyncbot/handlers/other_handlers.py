from aiogram import F, Router
from aiogram.filters import KICKED, MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message

# from ..models import UserTable

# init router a level of module
router = Router()
router.message.filter(F.chat.type == "private")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated) -> None:
    pass
    # db: UserTable = UserTable("data/database.db")
    # db.update_user_active((event.from_user.id,))


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def process_user_unblocked_bot(event: ChatMemberUpdated) -> None:
    await event.answer("Добро пожаловать обратно!)")
    # db: UserTable = UserTable("data/database.db")
    # db.update_user_active((event.from_user.id,))


@router.message()
async def send_echo(message: Message) -> None:
    await message.answer("Мне не удалось определить ссылку :(")
