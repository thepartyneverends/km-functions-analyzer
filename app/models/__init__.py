"""
Модели данных Pydantic.
"""
from .vacancy import Vacancy, Employer, Area, Salary, Snippet, KeySkill
from .response import (
    VacanciesResponse,
    TotalStatsResponse,
    CompanyStatsResponse,
    TopSkillsResponse,
    SearchResponse,
    MessageResponse
)

__all__ = [
    'Vacancy',
    'Employer',
    'Area',
    'Salary',
    'Snippet',
    'KeySkill',
    'VacanciesResponse',
    'TotalStatsResponse',
    'CompanyStatsResponse',
    'TopSkillsResponse',
    'SearchResponse',
    'MessageResponse'
]