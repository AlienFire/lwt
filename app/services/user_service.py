from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schema import UserFilterEntity, UserOut


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: int) -> User | None:
        return await self._session.get(entity=User, ident=id)

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
    ) -> User | None:
        stmt = select(User)
        stmt = select(User).where(User.username == username)
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
