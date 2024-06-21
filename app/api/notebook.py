from fastapi import APIRouter, Depends, status

from app.db.models import User
from app.di.auth import get_auth_user
from app.di.services import get_notebook_service
from app.schema import NotebookInto, NotebookOut
from app.services import NotebookService

notebook_router = APIRouter()


@notebook_router.post("/notebook")
async def create_note(
    note_data: NotebookInto,
    services: NotebookService = Depends(get_notebook_service),
    author: User = Depends(get_auth_user),
) -> NotebookOut:

    return await services.create_note(
        header=note_data.header,
        note=note_data.note,
        author=author,
    )


@notebook_router.get("/get_all")
async def get_all(
    services: NotebookService = Depends(get_notebook_service),
    author: User = Depends(get_auth_user),
):
    objects = await services.get_notes_by_author(author=author)
    return NotebookOut.model_validate_list(objects)


@notebook_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,)
async def delete_all_notes_of_author(
    id: int,
    services: NotebookService = Depends(
        get_notebook_service,
    ),
    author: User = Depends(get_auth_user),
) -> None:
    return await services.delete_note(
        id=id,
        author=author,
    )


@notebook_router.patch("/update_notebook")
async def update_note_or_header(
    id: int,
    data: NotebookInto,
    service: NotebookService = Depends(get_notebook_service),
    author: User = Depends(get_auth_user),
) -> NotebookOut:
    update_notebook = await service.change_note_or_header(id=id, data=data, author=author)
    return NotebookOut.model_validate(update_notebook, from_attributes=True)
