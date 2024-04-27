from typing import TypeVar

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.di.datebase import get_session
from app.servises import ContentService, UserService

ServiceT = TypeVar("ServiceT")


def get_service(
    service: type[ServiceT],
):
    def create_service(
        session=Depends(get_session),
    ) -> ServiceT:
        return service(session=session)

    return Depends(create_service)


def get_user_service(session=Depends(get_session)) -> UserService:

    return UserService(session=session)

def get_content_service(
    session: AsyncSession = Depends(get_session),
) -> ContentService:
    return ContentService(session=session)


