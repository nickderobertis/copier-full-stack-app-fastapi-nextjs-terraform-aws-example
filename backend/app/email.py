import asyncio

from aioyagmail import AIOSMTP
from logger import log
from settings.main import SETTINGS


async def send_single(to: str, subject: str, body: str) -> None:
    # walks you through oauth2 process if no file at this location
    async with AIOSMTP(
        user=SETTINGS.email_user, password=SETTINGS.email_password
    ) as yag:
        log.info(f"Sending email {subject} to {to}")
        await yag.send(to=to, subject=subject, contents=body)


if __name__ == "__main__":
    asyncio.run(
        send_single("derobertis.nick@gmail.com", "Test Email", "This is a test")
    )
