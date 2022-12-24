from app.auth.db import User
from app.auth.router import current_active_user
from app.auth.user_manager import UserManager, get_user_manager
from fastapi import APIRouter, Depends
from pydantic import BaseModel

delete_me_router = APIRouter()


class DeleteMeResponse(BaseModel):
    message: str


@delete_me_router.delete("/me", response_model=DeleteMeResponse)
async def delete_me(
    user: User = Depends(current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> DeleteMeResponse:
    await user_manager.delete(user)
    return DeleteMeResponse(message="success")
