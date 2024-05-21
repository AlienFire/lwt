from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.api.auth import (ACCESS_TOKEN_EXPIRE_MINUTES, Token,
                          create_access_token, get_current_active_user,
                          get_current_user, get_password_hash,
                          get_user_service, pwd_context)
from app.di.filters import get_user_filter
from app.di.services import get_user_service
from app.servises import UserFilterEntity, UserOut, UserService

user_router = APIRouter()


@user_router.get("/")
async def get_all_users(
    service: UserService = Depends(get_user_service),
    filter_: UserFilterEntity = Depends(get_user_filter),
) -> list[UserOut]:
    results = await service.get_users(filter_=filter_)
    return results


@user_router.get("/{id}")
async def get_one_user(
    id: int,
    service: UserService = Depends(get_user_service),
) -> UserOut:
    return await service.get_one_user(id=id)


@user_router.post("/find")
async def search_user(
    username: str,
    password: str,
    service: UserService = Depends(get_user_service),
    check_user: UserService = Depends(get_current_user),
) -> UserOut | None:
    # hash_password = get_password_hash(password=password)
    user = await service.find_user(username=username)
    if user:
        if pwd_context.verify(password, user.password):
            return UserOut.model_validate(user)

    raise HTTPException(
        status_code=400,
        detail="username or password is incorrect",
    )


@user_router.post("/")
async def create_new_user(
    username: str,
    password: str,
    service: UserService = Depends(get_user_service),
) -> UserOut:
    hash_password = get_password_hash(password=password)
    user = await service.find_user(username=username)
    if user:
        raise HTTPException(
            status_code=500,
            detail="This user is exist",
        )
    return await service.create_user(username=username, password=hash_password)


@user_router.delete("/{id}/delete")
async def delete_user(
    id: int,
    service: UserService = Depends(get_user_service),
) -> None:
    return await service.delete_user(id=id)


@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    servises: UserService = Depends(get_user_service),
) -> Token:
    user = await servises.find_user(username=form_data.username)
    # user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
