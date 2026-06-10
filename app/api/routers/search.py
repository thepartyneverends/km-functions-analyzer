"""
Роутер для эндпоинтов /search.
"""
from fastapi import APIRouter
from app.models.response import SearchResponse
from app.core.vacancy_processor import search_vacancies_by_keyword

router = APIRouter(prefix="/search", tags=["Поиск"])


@router.get("/{keyword}", response_model=SearchResponse)
async def search_vacancies(keyword: str):
    """
    Поиск вакансий по ключевому слову в названии.
    """
    found = search_vacancies_by_keyword(keyword)

    return SearchResponse(
        keyword=keyword,
        found_count=len(found),
        vacancies=found
    )