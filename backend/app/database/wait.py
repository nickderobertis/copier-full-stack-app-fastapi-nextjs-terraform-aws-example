"""Script that checks and waits for db to be available
"""
import asyncio
import time

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def check_db_availability(
    db_url, db_name="MainDB", total_wait_time=20, sleep_time=1
):
    while total_wait_time > 0:
        try:
            engine = create_async_engine(db_url)
            async with engine.begin() as conn:
                result = await conn.execute(text("SELECT * from pg_stat_activity"))
                success = result.fetchall()
            if success:
                print(f"{db_name} is ready, continuing app start...")
                break
            else:
                print(f"Waiting for {db_name} to be available...")
                time.sleep(sleep_time)
                total_wait_time -= sleep_time
        except (sqlalchemy.exc.OperationalError, ConnectionRefusedError):
            print(f"Waiting for {db_name} to be available...")
            time.sleep(sleep_time)
            total_wait_time -= sleep_time

    if total_wait_time <= 0:
        raise ConnectionError(
            f"Timed out while waiting to connect to the {db_name}. "
            "Please inspect the db logs for more information."
        )


if __name__ == "__main__":
    from settings.db import DB_SETTINGS

    asyncio.run(check_db_availability(DB_SETTINGS.uri, db_name="MainDB"))
