from fastapi import APIRouter, Depends

from app.di.filters import get_content_filter
from app.di.services import get_content_service
from app.schema import ContentInput, ContentOut, ContentFilterEntity
from app.services import ContentService
from app.db.models import User
from app.di.auth import get_auth_user

content_router = APIRouter()


@content_router.get("/")
async def get_all_content(
    filter_: ContentFilterEntity = Depends(get_content_filter),
    service: ContentService = Depends(get_content_service),
    auth_user: User = Depends(get_auth_user),
) -> list[ContentOut]:
    results = await service.get_contents(filter_=filter_)
    return results


@content_router.get("/{id}")
async def get_one_content(
    id: int,
    service: ContentService = Depends(get_content_service),
    auth_user: User = Depends(get_auth_user),
) -> ContentOut:
    result = await service.get_content(ident=id)
    return ContentOut.model_validate(result, from_attributes=True)


@content_router.post(
    "/",
    description="You can add information in content",
)
async def add_content(
    payload: ContentInput,
    service: ContentService = Depends(get_content_service),
) -> ContentOut:
    new_content = await service.create_content(name=payload.name)
    return ContentOut.model_validate(new_content, from_attributes=True)


@content_router.put(
    "/{id}",
    description="You can change information in content",
)
async def change_content(
    id: int,
    payload: ContentInput,
    service: ContentService = Depends(get_content_service),
    auth_user: User = Depends(get_auth_user),
):
    update_content = await service.update_content(id=id, name=payload.name)
    return ContentOut.model_validate(update_content, from_attributes=True)


@content_router.delete("/{id}")
async def delete_content(
    id: int,
    service: ContentService = Depends(get_content_service),
    auth_user: User = Depends(get_auth_user),
) -> None:
    await service.delete_content(id=id)
    return None
