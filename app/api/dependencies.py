"""
Общие зависимости для API роутеров.
"""
from typing import Annotated
from fastapi import Header, HTTPException


async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
    """
    Проверка API ключа (опционально, для будущего расширения).
    """
    # Здесь можно добавить проверку API ключа при необходимости
    # Пока что пропускаем все запросы
    return True


async def get_pagination_params(
    page: int = 1,
    per_page: int = 10
):
    """
    Получить параметры пагинации.
    """
    offset = (page - 1) * per_page
    return {"limit": per_page, "offset": offset}