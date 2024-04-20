from collections.abc import Sequence
from datetime import datetime
from typing import TypeVar

from fastapi import Body, Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import async_session, get_session
from app.db.models import Content, User
from app.routes import router
from app.schema import ContentFilterEntity, ContentInput, ContentOut, UserFilterEntity, UserOut
from app.servises import ContentService, UserService

ServiceT = TypeVar("ServiceT")

app = FastAPI()


app.include_router(router)


def get_service(
    service: type[ServiceT],
):
    def create_service(
        session: AsyncSession = Depends(get_session),
    ) -> ServiceT:
        return service(session=session)

    return Depends(create_service)


def get_content_service(
    session: AsyncSession = Depends(get_session),
) -> ContentService:
    return ContentService(session=session)


def get_content_filter(
    name: str | None = Query(None, description="Фильтр по названию медиа контента"),
) -> ContentFilterEntity:
    return ContentFilterEntity(name=name)


def get_user_filter(
    username: str | None = Query(None, description="Фильтр по логину"),
) -> UserFilterEntity:
    return UserFilterEntity(username=username)


@app.get("/users/")
async def get_all_users(
    # service: UserService = Depends(get_content_service),
    service: UserService = get_service(UserService),
    filter_: UserFilterEntity = Depends(get_user_filter),
) -> list[UserOut]:
    results = await service.get_users(filter_=filter_)
    return results


# @app.get("/users/")
# async def get_all_users():
#     session = async_session()
#     stmt = select(User)

#     list_of_users = (await session.scalars(stmt)).all()

#     return [UserOut(id=c.id, username=c.username, created_at=c.created_at) for c in list_of_users]


@app.get("/user/{id}")
async def get_one_user(
    id: int,
    service: UserService = get_service(UserService),
) -> UserOut:
    return await service.get_one_user(id=id)


@app.post("/user/")
async def create_new_user(
    username: str,
    password: str,
    service: UserService = get_service(UserService),
) -> UserOut:
    return await service.create_user(username=username, password=password)


@app.delete("/delete/{id}")
async def delete_user(
    id: int,
    service: UserService = get_service(UserService),
) -> None:
    return await service.delete_user(id=id)


@app.get("/contents/")
async def get_all_content(
    filter_: ContentFilterEntity = Depends(get_content_filter),
    service: ContentService = Depends(get_content_service),
) -> list[ContentOut]:
    results = await service.get_contents(filter_=filter_)
    # return [ContentOut.model_validate(table_row, from_attributes=True) for table_row in results]
    return results


@app.get("/contents/{id}")
async def get_one_content(
    id: int,
    service: ContentService = Depends(get_content_service),
) -> ContentOut:
    result = await service.get_content(ident=id)
    return ContentOut.model_validate(result, from_attributes=True)


@app.post(
    "/contents/",
    description="You can add information in content",
)
async def add_content(
    payload: ContentInput,
    service: ContentService = Depends(get_content_service),
    # name: str = Body(
    #     description="This is the name of content",
    #     min_length=1,
    #     max_length=200,
    # ),
) -> ContentOut:
    # new_content = Content(name=payload.name)
    new_content = await service.create_content(name=payload.name)
    # session = async_session()
    # session.add(new_content)
    # await session.commit()
    return ContentOut.model_validate(new_content, from_attributes=True)


@app.put(
    "/contents/{id}",
    description="You can change information in content",
)
async def change_content(
    id: int,
    payload: ContentInput,
    service: ContentService = Depends(get_content_service),
):
    update_content = await service.update_content(id=id, name=payload.name)
    return ContentOut.model_validate(update_content, from_attributes=True)


@app.delete("/contents/{id}")
async def delete_content(
    id: int,
    service: ContentService = Depends(get_content_service),
) -> None:
    await service.delete_content(id=id)
    return None


# @app.patch("/content/{id}", description="If you want to make edits")
# async def change_content_partially(
#     id: int,
#     name: str = Body(
#         description="This is new name of content",
#         min_length=1,
#         max_length=200,
#     ),
# ):
#     session = async_session()
#     content = await session.get(entity=Content, ident=id)
#     if content is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Id={id} is not exist",
#         )
#     return []
