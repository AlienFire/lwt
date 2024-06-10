from fastapi import APIRouter, Depends, HTTPException

from app.db.models import User
from app.di.auth import get_auth_user
from app.di.filters import get_user_filter
from app.di.services import get_user_service
from app.schema import UserFilterEntity, UserIn, UserOut
from app.services.auth_services import AuthorizationService
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.get("/")
async def get_all_users(
    service: UserService = Depends(get_user_service),
    filter_: UserFilterEntity = Depends(get_user_filter),
    auth_user: User = Depends(get_auth_user),
) -> list[UserOut]:
    results = await service.get_users(filter_=filter_)
    return results


@user_router.get("/me")
async def get_me(auth_user: User = Depends(get_auth_user)) -> UserOut:
    return UserOut.model_validate(auth_user, from_attributes=True)


@user_router.get("/{id}")
async def get_one_user(
    id: int,
    service: UserService = Depends(get_user_service),
) -> UserOut:
    return await service.get_one_user(id=id)


@user_router.post("/")
async def create_new_user(
    user_data: UserIn,
    service: UserService = Depends(get_user_service),
) -> UserOut:
    user = await service.find_user(username=user_data.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This user is exist",
        )
    hash_password = AuthorizationService.get_password_hash(password=user_data.password)
    return await service.create_user(username=user_data.username, password=hash_password)


@user_router.delete("/{id}/delete")
async def delete_user(
    id: int,
    service: UserService = Depends(get_user_service),
    auth_user: User = Depends(get_auth_user),
) -> None:
    return await service.delete_user(id=id)
