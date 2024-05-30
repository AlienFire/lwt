from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Content
from app.schema import (
    ContentFilterEntity,
    ContentOut,
)


class ContentService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_contents(self, filter_: ContentFilterEntity) -> list[ContentOut]:
        stmt = select(Content)
        if filter_.name is not None:
            # stmt = stmt.where(Content.name.ilike(f"%{name}%"))
            stmt = stmt.where(Content.name.ilike(f"%{filter_.name}%"))
        list_of_content = (await self._session.scalars(stmt)).all()
        return ContentOut.model_validate_list(objs=list_of_content)
        return [
            ContentOut(
                name=c.name,
                id=c.id,
                created_at=c.created_at,
            )
            for c in list_of_content
        ]

    async def get_content(self, ident: int) -> Content:
        obj = await self._session.get(Content, ident=ident)
        if obj is None:
            raise HTTPException(
                status_code=404,
                detail=f"Content with id={ident} is not found",
            )
        return obj

    async def create_content(self, name: str) -> Content:
        object = Content(name=name)
        self._session.add(object)
        await self._session.commit()
        return object

    async def update_content(
        self,
        id: int,
        name: str,
    ) -> Content:
        obj = await self._session.get(Content, ident=id)
        if obj is None:
            raise HTTPException(
                status_code=404,
                detail=f"Content with id={id} is not found",
            )
        obj.name = name
        self._session.add(obj)
        await self._session.commit()
        return obj

    async def delete_content(self, id: int) -> None:
        object = await self._session.get(Content, ident=id)
        if object is None:
            raise HTTPException(
                status_code=404,
                detail=f"Content with id={id} is not found",
            )
        await self._session.delete(object)
        await self._session.commit()
        return None
