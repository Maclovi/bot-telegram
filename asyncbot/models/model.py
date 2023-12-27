from datetime import datetime
from typing import Annotated, Literal, Optional

from sqlalchemy import BigInteger, ForeignKey, String, create_engine, func
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship, sessionmaker)

from ..data.settings import secrets

engine = create_engine(url=f'postgresql+psycopg{secrets.URL_POSTGRES}')
Session = sessionmaker(engine)

intpk = Annotated[int, mapped_column(primary_key=True)]
big_int_unique = Annotated[int, mapped_column(BigInteger, unique=True)]
str_50 = Annotated[str, mapped_column(String(50))]
str_50_unique = Annotated[str, mapped_column(String(50), unique=True)]
datetime_default = Annotated[
    datetime,
    mapped_column(server_default=func.current_timestamp()),
]
datetime_update = Annotated[datetime, mapped_column(onupdate=datetime.utcnow)]
status = Literal['active', 'inactive']


class Base(DeclarativeBase):
    id: Mapped[intpk]


class UserOrm(Base):
    __tablename__ = 'user'
    user_id: Mapped[big_int_unique]
    first_name: Mapped[Optional[str_50]]
    last_name: Mapped[Optional[str_50]]
    username: Mapped[Optional[str_50]]
    status: Mapped[status]
    created_at: Mapped[datetime_default]
    updated_at: Mapped[Optional[datetime_update]]

    files: Mapped[list["FileOrm"]] = relationship(
        back_populates="users", secondary="user_file"
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"\tid: {self.id}\n"
            f"\tuser_id: {self.user_id}\n"
            f"\tfirst_name: {self.first_name}\n"
            f"\tlast_name: {self.last_name}\n"
            f"\tusername: {self.username}\n"
            f"\tstatus: {self.status}\n"
            f"\tcreated_at: {self.created_at}\n"
            f"\tupdated_at: {self.updated_at}\n)"
        )


class FileOrm(Base):
    __tablename__ = 'file'
    video_id: Mapped[str_50_unique]
    file_id: Mapped[str_50]
    created_at: Mapped[datetime_default]
    updated_at: Mapped[Optional[datetime_update]]

    users: Mapped[list["UserOrm"]] = relationship(
        back_populates="files", secondary="user_file"
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"\tid: {self.id}\n"
            f"\tvideo_id: {self.video_id}\n"
            f"\tfile_id: {self.file_id}\n)"
            f"\tcreated_at: {self.created_at}\n"
            f"\tupdated_at: {self.updated_at}\n)"
        )


class UserFileOrm(Base):
    __tablename__ = 'user_file'
    user_fk: Mapped[int] = mapped_column(
        ForeignKey('user.id', ondelete="CASCADE"),
    )
    file_fk: Mapped[int] = mapped_column(
        ForeignKey('file.id', ondelete="CASCADE"),
    )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"\tid: {self.id}\n"
            f"\tuser_fk: {self.user_fk}\n"
            f"\tfile_fk: {self.file_fk}\n)"
        )


Base.metadata.create_all(engine)
