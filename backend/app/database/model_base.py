from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

common_id_kwargs = dict(default_factory=lambda: str(uuid4()))


def IDField(**kwargs) -> Field:
    all_kwargs = {**common_id_kwargs, **kwargs}
    return Field(**all_kwargs)


class IDTableModelMixin(SQLModel):
    id: Optional[UUID] = Field(**common_id_kwargs, primary_key=True, nullable=False)
