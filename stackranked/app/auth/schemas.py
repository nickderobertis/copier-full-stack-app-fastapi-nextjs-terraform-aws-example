import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class UserMixin(BaseModel):
    name: str


class UserRead(UserMixin, schemas.BaseUser[uuid.UUID]):
    has_real_password: bool


class UserCreate(UserMixin, schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    name: str | None = None
