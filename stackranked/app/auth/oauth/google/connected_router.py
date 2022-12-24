from app.auth.db import OAuthAccount, User
from app.auth.router import current_active_user
from app.database.engine import get_async_session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ConnectedAccounts(BaseModel):
    connected_emails: list[str]


def create_google_connected_router() -> APIRouter:
    router = APIRouter()

    @router.get("/connected", response_model=ConnectedAccounts)
    async def connected(
        user: User = Depends(current_active_user),
        session: AsyncSession = Depends(get_async_session),
    ) -> ConnectedAccounts:
        # Query OAuthAccount with async sqlalchemy
        statement = (
            select(OAuthAccount)
            .where(OAuthAccount.user_id == user.id)
            .where(OAuthAccount.oauth_name == "google")
        )
        result = await session.execute(statement)
        accounts = result.scalars().all()
        connected_emails = [account.account_email for account in accounts]
        return ConnectedAccounts(connected_emails=connected_emails)

    return router
