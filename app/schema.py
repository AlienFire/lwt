from typing import Self, TypeVar
from collections.abc import Sequence
from pydantic import BaseModel, Field
from datetime import datetime
from app.db.models import Base

DBModelT = TypeVar("DBModelT", bound=Base)


class BaseEntity(BaseModel):
    model_config = {"from_attributes": True}

    @classmethod
    def model_validate_list(cls, objs: Sequence[DBModelT]) -> list[Self]:
        return [cls.model_validate(obj) for obj in objs]


class BaseContent(BaseModel):
    """Базовая схема для Content"""

    name: str = Field(..., description="Название медиа контента")


class ContentInput(BaseContent):
    """Схема данных для создания Content"""

    pass


class ContentOut(BaseEntity):
    """Схема данных для вывода Content"""

    id: int
    created_at: datetime


class ContentFilterEntity(BaseModel):
    """Сущность фильтра Content"""

    name: str | None = Field(None, description="Фильтр по названию медиа контента")


class UserFilterEntity(BaseModel):
    """Сущность фильтра User"""

    username: str | None = Field(None, description="Фильтр по логину")


class UserOut(BaseEntity):
    """Схема данных для вывода User"""

    id: int
    username: str
    created_at: datetime
