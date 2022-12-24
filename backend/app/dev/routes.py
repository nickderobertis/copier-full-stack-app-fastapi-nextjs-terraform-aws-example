from fastapi import APIRouter

dev_router = APIRouter()


@dev_router.get("/error")
async def error():
    raise Exception("This is a test error")
