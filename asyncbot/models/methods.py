from typing import Any

from sqlalchemy import select

from ..data.settings import UserValidate
from ..services import services
from .model import FileOrm, Session, UserFileOrm, UserOrm, engine

IsNewUser = bool


class SyncCore:
    @classmethod
    def add_person(cls, data: UserValidate) -> IsNewUser:
        engine.echo = False
        with Session() as session:
            query = select(UserOrm).filter_by(user_id=data.user_id)
            user = session.scalars(query).one_or_none()
            if user is None:
                user = UserOrm(**data.model_dump())
                session.add(user)
                session.commit()
                return IsNewUser(True)
        return IsNewUser(False)

    @classmethod
    def add_user_file(cls, session, file: FileOrm, user_id: int) -> None:
        user: UserOrm = session.scalars(
            select(UserOrm)
            .filter_by(user_id=user_id)
        ).one()
        user_file: UserFileOrm | None = session.scalars(
            select(UserFileOrm)
            .filter_by(user_fk=user.id, file_fk=file.id)
        ).one_or_none()
        if user_file is None:
            file.users.append(user)

    @classmethod
    def get_file(cls, url: str, user_id: int) -> FileOrm | None:
        engine.echo = False
        video_id: str = services.video_id(url)
        with Session() as session:
            file = session.scalars(
                select(FileOrm).filter_by(video_id=video_id)
            ).one_or_none()
            if file:
                cls.add_user_file(session, file, user_id)
                session.commit()
                return file

    @classmethod
    async def add_file(cls, data: dict[str, Any]) -> None:
        engine.echo = False
        video_id: str = data["video_id"]
        file_id: str = data["file_id"]
        user_id: int = data["user_id"]
        caption: str = data["caption"]
        with Session() as session:
            file = FileOrm(video_id=video_id, file_id=file_id, caption=caption)
            session.add(file)
            cls.add_user_file(session, file, user_id)
            session.commit()

    @classmethod
    def update_person(cls, data: UserValidate) -> None:
        engine.echo = False
        with Session() as session:
            query = select(UserOrm).filter_by(user_id=data.user_id)
            user = session.scalars(query).one()
            user.first_name = data.first_name
            user.last_name = data.last_name
            user.username = data.username
            user.status = data.status
            session.add(user)
            session.commit()
