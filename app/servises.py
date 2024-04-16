from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Content
from app.schema import ContentFilterEntity


class ContentService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_contents(self, filter_: ContentFilterEntity) -> Sequence[Content]:
        stmt = select(Content)
        if filter_.name is not None:
            # stmt = stmt.where(Content.name.ilike(f"%{name}%"))
            stmt = stmt.where(Content.name.ilike(f"%{filter_.name}%"))

        return (await self._session.scalars(stmt)).all()

    async def get_content(self, ident: int) -> Content:
        obj = await self._session.get(Content, ident=ident)
        if obj is None:
            raise HTTPException(
                status_code=404,
                detail=f"Content with id={id} is not found",
            )
        return obj