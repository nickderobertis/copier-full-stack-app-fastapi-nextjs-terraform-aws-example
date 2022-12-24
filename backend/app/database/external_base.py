"""
Sets up the base metadata for alembic migrations, by importing all the models
as well combining the metadata from the SQLAlchemy Base and the SQLModel Base
into a single metadata object.
"""
from typing import Final

import app.all_models  # noqa: F401
from app.auth.db import Base as AuthBase
from sqlalchemy import MetaData
from sqlmodel import SQLModel as SQLModelBase


def merge_metadata(*original_metadata) -> MetaData:
    merged = MetaData()

    for original_metadatum in original_metadata:
        for table in original_metadatum.tables.values():
            table.to_metadata(merged)

    return merged


metadata: Final[MetaData] = merge_metadata(AuthBase.metadata, SQLModelBase.metadata)
