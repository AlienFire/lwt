from fastapi import APIRouter
from .users import user_router
from .content import content_router
from .auth import auth_router

root_router = APIRouter()


@root_router.get("/")
async def hello():
    return {"message": "Hello"}


root_router.include_router(
    user_router,
    prefix="/users",
)

root_router.include_router(
    content_router,
    prefix="/contents",
)

root_router.include_router(
    auth_router,
    prefix="/auth",
)
