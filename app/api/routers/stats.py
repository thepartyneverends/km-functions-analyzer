"""
Роутер для эндпоинтов /stats.
"""
from fastapi import APIRouter
from app.models.response import TotalStatsResponse, CompanyStatsResponse
from app.core.statistics import calculate_total_stats, calculate_companies_stats, calculate_salary_stats

router = APIRouter(prefix="/stats", tags=["Статистика"])


@router.get("/total", response_model=TotalStatsResponse)
async def get_total_stats():
    """
    Получить общую статистику по вакансиям.
    """
    return calculate_total_stats()


@router.get("/companies", response_model=CompanyStatsResponse)
async def get_companies_stats():
    """
    Получить статистику по компаниям (сколько вакансий от каждой).
    """
    return calculate_companies_stats()


@router.get("/salary")
async def get_salary_stats():
    """
    Получить статистику по зарплатам.
    """
    return calculate_salary_stats()