from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models import Content, User
from app.schema import (
    ContentFilterEntity,
    ContentOut,
)


class ContentService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_contents(self, filter_: ContentFilterEntity) -> list[ContentOut]:
        stmt = select(Content).options(joinedload(Content.author))
        if filter_.name is not None:
            stmt = stmt.where(Content.name.ilike(f"%{filter_.name}%"))
        list_of_content = (await self._session.scalars(stmt)).all()
        return ContentOut.model_validate_list(objs=list_of_content)

    async def get_content(self, ident: int) -> Content:
        obj = await self._session.get(
            Content,
            ident=ident,
            options=[
                joinedload(Content.author),
            ],
        )
        if obj is None:
            raise HTTPException(
                status_code=404,
                detail=f"Content with id={ident} is not found",
            )
        return obj

    async def create_content(
        self,
        name: str,
        author: User,
    ) -> Content:
        object = Content(
            name=name,
            user_id=author.id,
        )
        self._session.add(object)
        await self._session.commit()
        return object

    async def update_content(
        self,
        id: int,
        name: str,
        auth_user: User,
    ) -> Content:
        content = await self.get_content(ident=id)

        if content.user_id != auth_user.id:
            raise HTTPException(
                status_code=403,
                detail=f"You haven't rights to change note with id={id}",
            )
        content.name = name
        self._session.add(content)
        await self._session.commit()
        return content

    async def delete_content(
        self,
        id: int,
        auth_user: User,
    ) -> None:

        content = await self.get_content(ident=id)
        if content.user_id != auth_user.id:
            raise HTTPException(
                status_code=403,
                detail=f"You haven't rights to change note with id={id}",
            )
        await self._session.delete(content)
        await self._session.commit()
        return None
