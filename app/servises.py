from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Content, User
from app.schema import ContentFilterEntity, ContentOut, UserFilterEntity, UserOut


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_users(self, filter_: UserFilterEntity) -> list[UserOut]:
        stmt = select(User)
        if filter_.username is not None:
            stmt = select(User).where(User.username.ilike(f"%{filter_.username}%"))
        list_of_users = (await self._session.scalars(stmt)).all()
        return UserOut.model_validate_list(objs=list_of_users)

    async def get_one_user(self, id: int) -> UserOut:
        stmt = await self._session.get(entity=User, ident=id)
        if stmt is None:
            raise HTTPException(
                status_code=404,
                detail=f"User with id={id} not found",
            )
        return UserOut.model_validate(obj=stmt)

    async def find_user(
        self,
        username: str,
        password: str,
    ) -> User | None:
        stmt = select(User)
        stmt = select(User).where(
            User.username == username,
            User.password == password,
        )
        return await self._session.scalar(stmt)

    async def create_user(
        self,
        username: str,
        password: str,
    ) -> UserOut:
        object = User(username=username, password=password)
        self._session.add(object)
        await self._session.commit()
        return object

    async def delete_user(self, id: int) -> None:
        stmt = await self._session.get(entity=User, ident=id)
        if stmt is None:
            raise HTTPException(
                status_code=404,
                detail="User with id={id} not found",
            )
        await self._session.delete(instance=stmt)
        await self._session.commit()
        return None


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
