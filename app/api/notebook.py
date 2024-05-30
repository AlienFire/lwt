from fastapi import APIRouter, Depends

from app.di.services import get_notebook_service
from app.schema import NotebookOut, NotebookInto
from app.services import NotebookService

notebook_router = APIRouter()


@notebook_router.post("/notebook")
async def create_note(
    header: str,
    note: str,
    services: NotebookService = Depends(get_notebook_service),
) -> NotebookOut:
    author = "test_author"

    return await services.create_note(
        header=header,
        note=note,
        author=author,
    )


@notebook_router.get("/get_all")
async def get_all(
    author: str = "",
    services: NotebookService = Depends(get_notebook_service),
):
    objects = await services.get_notes_by_author(author=author)
    return NotebookOut.model_validate_list(objects)


@notebook_router.delete("/{id}")
async def delete_all_notes_of_author(
    id: int,
    services: NotebookService = Depends(
        get_notebook_service,
    ),
) -> None:
    return await services.delete_note(id=id)


@notebook_router.patch("/update_notebook")
async def update_note_or_header(
    id: int,
    data: NotebookInto,
    service: NotebookService = Depends(get_notebook_service),
) -> NotebookOut:
    update_notebook = await service.change_note_or_header(
        id=id,
        data=data,
    )
    return NotebookOut.model_validate(update_notebook, from_attributes=True)
