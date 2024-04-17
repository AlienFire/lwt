from fastapi import FastAPI, HTTPException, Query, Body, status, Depends
from app.routes import router
from app.schema import ContentOut, ContentInput, ContentFilterEntity
from datetime import datetime
from app.db.connection import get_session, async_session
from app.db.models import Content
from app.servises import ContentService
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import Sequence

app = FastAPI()


app.include_router(router)


def get_content_service(
    session: AsyncSession = Depends(get_session),
) -> ContentService:
    return ContentService(session=session)


def get_content_filter(
    name: str | None = Query(None, description="Фильтр по названию медиа контента"),
) -> ContentFilterEntity:
    return ContentFilterEntity(name=name)


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


@app.delete(
    "/contents/{id}", status_code=status.HTTP_204_NO_CONTENT, description="This is description"
)
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
