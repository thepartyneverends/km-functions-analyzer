"""
Модели ответов API.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.models.vacancy import Vacancy


class VacanciesResponse(BaseModel):
    """Ответ со списком вакансий."""
    total: int
    limit: int
    offset: int
    vacancies: List[Vacancy]

    class Config:
        json_schema_extra = {
            "example": {
                "total": 5,
                "limit": 10,
                "offset": 0,
                "vacancies": []
            }
        }


class TotalStatsResponse(BaseModel):
    """Ответ с общей статистикой."""
    total_vacancies: int
    vacancies_with_salary: int
    vacancies_without_salary: int
    unique_companies: int
    salary_percentage: float


class CompanyStatsResponse(BaseModel):
    """Ответ со статистикой по компаниям."""
    total_companies: int
    companies: List[Dict[str, Any]]


class TopSkillsResponse(BaseModel):
    """Ответ с топ-навыками."""
    total_unique_skills: int
    top_skills: List[Dict[str, Any]]


class SearchResponse(BaseModel):
    """Ответ на поиск."""
    keyword: str
    found_count: int
    vacancies: List[Dict[str, Any]]


class MessageResponse(BaseModel):
    """Простой ответ с сообщением."""
    message: str
    status: str = "success"