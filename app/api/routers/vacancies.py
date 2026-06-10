"""
Роутер для эндпоинтов /vacancies.
"""
from fastapi import APIRouter, HTTPException, Query
from app.models.vacancy import Vacancy
from app.models.response import VacanciesResponse
from app.core.vacancy_processor import get_vacancies_paginated, get_vacancy_by_id
from app.config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

router = APIRouter(prefix="/vacancies", tags=["Вакансии"])


@router.get("/", response_model=VacanciesResponse)
async def get_vacancies(
        limit: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Количество вакансий"),
        offset: int = Query(0, ge=0, description="Смещение (пагинация)")
):
    """
    Получить список вакансий с пагинацией.
    """
    vacancies_list, total = get_vacancies_paginated(limit, offset)

    return VacanciesResponse(
        total=total,
        limit=limit,
        offset=offset,
        vacancies=vacancies_list
    )


@router.get("/{vacancy_id}", response_model=Vacancy)
async def get_vacancy_by_id_endpoint(vacancy_id: str):
    """
    Получить конкретную вакансию по её ID.
    """
    vacancy = get_vacancy_by_id(vacancy_id)

    if not vacancy:
        raise HTTPException(status_code=404, detail=f"Вакансия с ID {vacancy_id} не найдена")

    return vacancy