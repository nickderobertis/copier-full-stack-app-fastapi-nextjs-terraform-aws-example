from typing import Any

from app.database.engine import get_async_session
from fastapi import Depends
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import Boolean, Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Any = declarative_base()


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    name: str = Column(String, nullable=False)  # type: ignore
    oauth_accounts: list[OAuthAccount] = relationship(  # type: ignore
        "OAuthAccount", lazy="joined", cascade="all, delete-orphan"
    )
    has_real_password: bool = Column(  # type: ignore
        Boolean, default=True, nullable=False, server_default="t"
    )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
