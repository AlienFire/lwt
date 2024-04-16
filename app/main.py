# from collections.abc import Sequence
# from datetime import datetime

from fastapi import Body, Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.connection import async_session, get_session
from app.db.models import Content
from app.routes import router
from app.schema import ContentFilterEntity, ContentInput, ContentOut
from app.servises import ContentService

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
    return [ContentOut.model_validate(table_row, from_attributes=True) for table_row in results]


@app.get("/contents/{id}")
async def get_one_content(id: int) -> ContentOut:
    session = async_session()
    stmt = select(Content).where(Content.id == id)
    # r = await session.get(entity=Content, ident=id)
    result = await session.scalar(stmt)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Content with id={id} is not found",
        )
    return ContentOut.model_validate(result, from_attributes=True)


@app.post("/contents/")
async def add_content(
    payload: ContentInput,
    # name: str = Body(
    #     description="This is the name of content",
    #     min_length=1,
    #     max_length=200,
    # ),
):
    new_content = Content(name=payload.name)
    session = async_session()
    session.add(new_content)
    await session.commit()
    return ContentOut.model_validate(new_content, from_attributes=True)


@app.put("/contents/{id}")
async def change_content(
    id: int,
    name: str = Body(
        description="This is new name of content",
        min_length=1,
        max_length=200,
    ),
):
    session = async_session()
    content = await session.get(entity=Content, ident=id)
    if content is None:
        raise HTTPException(
            status_code=404,
            detail=f"Content with id={id} is not found",
        )
    # stmt = (
    #     update(Content)
    #     .where(Content.id == id)
    #     .values(name=name)
    #     .returning(3
    #         Content.id,
    #         Content.name,
    #         Content.created_at,
    #     )
    # )
    # result = (await session.execute(stmt)).one_or_none()
    content.name = name
    session.add(content)
    await session.commit()
    return ContentOut.model_validate(content, from_attributes=True)
    # session.add()


@app.delete(
    "/contents/{id}", status_code=status.HTTP_204_NO_CONTENT, description="This is description"
)
async def delete_content(
    id: int,
):
    session = async_session()
    content = await session.get(entity=Content, ident=id)
    if content is None:
        raise HTTPException(
            status_code=404,
            detail=f"Id={id} is not exist",
        )
    # delete(Content).where(Content.id == id)
    # del Content[id]
    await session.delete(content)
    await session.commit()
    return None


@app.patch("/content/{id}", description="If you want to make edits")
async def change_content_partially(
    id: int,
    name: str = Body(
        description="This is new name of content",
        min_length=1,
        max_length=200,
    ),
):
    session = async_session()
    content = await session.get(entity=Content, ident=id)
    if content is None:
        raise HTTPException(
            status_code=404,
            detail=f"Id={id} is not exist",
        )
    return []
