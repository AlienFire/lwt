from fastapi import APIRouter, Depends, HTTPException

from app.api.auth import get_password_hash, pwd_context, verify_password
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
    username: str, password: str, service: UserService = Depends(get_user_service)
) -> UserOut | None:
    # hash_password = get_password_hash(password=password)
    user = await service.find_user(
        username=username
    )
    if user:
        if pwd_context. verify(password, user.password):
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
