"""
Роутер для эндпоинтов /skills.
"""
from fastapi import APIRouter, Query
from app.models.response import TopSkillsResponse
from app.core.statistics import calculate_top_skills

router = APIRouter(prefix="/skills", tags=["Навыки"])


@router.get("/top", response_model=TopSkillsResponse)
async def get_top_skills(
    limit: int = Query(10, ge=1, le=50, description="Количество навыков")
):
    """
    Получить топ наиболее часто встречающихся ключевых навыков.
    """
    return calculate_top_skills(limit)