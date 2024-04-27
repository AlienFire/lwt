from fastapi import Query

from app.servises import ContentFilterEntity, UserFilterEntity


def get_user_filter(
    username: str | None = Query(None, description="Фильтр по логину"),
) -> UserFilterEntity:
    return UserFilterEntity(username=username)


def get_content_filter(
    name: str | None = Query(None, description="Фильтр по названию медиа контента"),
) -> ContentFilterEntity:
    return ContentFilterEntity(name=name)