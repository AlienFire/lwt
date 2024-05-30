from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Notebook
from app.schema import (
    NotebookInto,
    NotebookOut,
)


class NotebookService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_note(
        self,
        header: str,
        note: str,
        author: str,
    ) -> NotebookOut:
        object = Notebook(
            header=header,
            note=note,
            author=author,
        )
        self._session.add(object)
        await self._session.commit()
        return object

    async def get_notes_by_author(self, author: str) -> list[NotebookOut]:
        stmt = select(Notebook).where(Notebook.author.ilike(f"%{author}%"))
        objects = (await self._session.scalars(stmt)).all()
        return NotebookOut.model_validate_list(objs=objects)

    async def delete_note(self, id: int) -> None:
        object = await self._session.get(Notebook, ident=id)
        if object is None:
            raise HTTPException(
                status_code=404,
                detail="Author is not found",
            )
        await self._session.delete(object)
        await self._session.commit()
        return None

    async def change_note_or_header(
        self,
        id: int,
        data: NotebookInto,
    ) -> NotebookInto:
        notebook = await self._session.get(Notebook, id)
        if notebook is None:
            raise HTTPException(status_code=404, detail="id={id} is not found")
        if data.header is not None:
            notebook.header = data.header
        if data.note is not None:
            notebook.note = data.note
        self._session.add(notebook)
        await self._session.commit()
        return notebook
