from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Notebook, User
from app.schema import (
    NotebookInto,
    NotebookOut,
)


class NotebookService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: int) -> Notebook | None:
        return await self._session.get(Notebook, ident=id)

    async def create_note(
        self,
        header: str,
        note: str,
        author: User,
    ) -> NotebookOut:
        object = Notebook(
            header=header,
            note=note,
            user_id=author.id,
        )
        self._session.add(object)
        await self._session.commit()
        return NotebookOut.model_validate(obj=object)

    async def get_notes_by_author(self, author: User) -> list[NotebookOut]:
        stmt = select(Notebook).where(Notebook.user_id == author.id)
        objects = (await self._session.scalars(stmt)).all()
        return NotebookOut.model_validate_list(objs=objects)

    async def delete_note(
        self,
        id: int,
        author: User,
    ) -> None:
        notebook = await self.get_by_id(id=id)
        if notebook is None:
            raise HTTPException(
                status_code=404,
                detail="Author is not found",
            )
        if notebook.user_id != author.id:
            raise HTTPException(
                status_code=403,
                detail="You haven't rights to change note with id={id}",
            )

        await self._session.delete(notebook)
        await self._session.commit()
        return None

    async def change_note_or_header(
        self,
        id: int,
        data: NotebookInto,
        author: User,
    ) -> NotebookInto:
        notebook = await self._session.get(Notebook, id)
        if notebook is None:
            raise HTTPException(status_code=404, detail="id={id} is not found")
        if notebook.author.id != author.id:
            raise HTTPException(
                status_code=403,
                detail="You haven't rights to change note with id={id}",
            )

        if data.header is not None:
            notebook.header = data.header
        if data.note is not None:
            notebook.note = data.note
        self._session.add(notebook)
        await self._session.commit()
        return notebook
