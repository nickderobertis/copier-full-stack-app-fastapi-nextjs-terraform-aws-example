import subprocess
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import pytest
from logger import log
from settings.main import SETTINGS
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from tests.config import PROJECT_DIR
from tests.dirutils import change_directory_to

db_host = SETTINGS.db.host

test_db_uri = f"postgresql+asyncpg://postgres:postgres@{db_host}/test"
test_engine = create_async_engine(test_db_uri)
test_async_session_maker = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


def run_migrations() -> None:
    with change_directory_to(PROJECT_DIR):
        alembic_args = [
            "--raiseerr",
            "-x",
            "db_url=" + test_db_uri,
            "upgrade",
            "head",
        ]
        result = subprocess.run(
            ["alembic", *alembic_args], check=True, capture_output=True
        )
        log.info(result.stdout.decode("utf-8"))


def create_test_db_and_tables():
    run_migrations()


async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session


@asynccontextmanager
async def create_test_database() -> AsyncGenerator[None, None]:
    # Log into postgres db (main db) so we can then create other dbs
    temp_uri = f"postgresql+asyncpg://postgres:postgres@{db_host}/postgres"
    temp_engine = create_async_engine(temp_uri)
    async with temp_engine.begin() as conn:
        await conn.execute(text("COMMIT"))
        # Handle prior bad test run that didn't clean up the db
        await conn.execute(text("DROP DATABASE IF EXISTS test"))
        await conn.execute(text("CREATE DATABASE test"))
    try:
        yield
    finally:
        async with temp_engine.begin() as conn:
            await conn.execute(text("COMMIT"))
            await conn.execute(text("DROP DATABASE test WITH (FORCE)"))


@pytest.fixture(scope="session")
async def test_db():
    async with create_test_database():
        create_test_db_and_tables()
        yield
