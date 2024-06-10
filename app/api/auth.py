from fastapi import APIRouter, Depends

from app.di.auth import get_auth_token
from app.schema import Token

auth_router = APIRouter()


@auth_router.post("/token/")
async def auth_token(token: Token = Depends(get_auth_token)) -> Token:
    return token
