from pydantic import BaseModel, Field
from datetime import datetime


class BaseContent(BaseModel):
    """Базовая схема для Content"""

    name: str = Field(..., description="Название медиа контента")


class ContentInput(BaseContent):
    """Схема данных для создания Content"""

    pass


class ContentOut(BaseContent):
    """Схема данных для вывода Content"""

    id: int
    created_at: datetime


class ContentFilterEntity(BaseModel):
    """Сущность фильтра Content"""

    name: str | None = Field(None, description="Фильтр по названию медиа контента")
