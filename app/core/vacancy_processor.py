"""
Обработка вакансий (фильтрация, поиск, пагинация).
"""
from typing import List, Dict, Any, Optional
from app.core.data_loader import get_vacancies


def get_all_vacancies() -> List[Dict[str, Any]]:
    """Возвращает все вакансии."""
    return get_vacancies()


def get_vacancy_by_id(vacancy_id: str) -> Optional[Dict[str, Any]]:
    """Возвращает вакансию по ID."""
    vacancies = get_all_vacancies()
    for vacancy in vacancies:
        if vacancy.get('id') == vacancy_id:
            return vacancy
    return None


def get_vacancies_paginated(limit: int, offset: int) -> tuple[List[Dict[str, Any]], int]:
    """
    Возвращает вакансии с пагинацией.

    Args:
        limit: Количество вакансий на страницу
        offset: Смещение (пропустить N вакансий)

    Returns:
        tuple: (список вакансий, общее количество)
    """
    vacancies = get_all_vacancies()
    total = len(vacancies)
    paginated = vacancies[offset:offset + limit]
    return paginated, total


def search_vacancies_by_keyword(keyword: str) -> List[Dict[str, Any]]:
    """
    Ищет вакансии по ключевому слову в названии.

    Args:
        keyword: Ключевое слово для поиска

    Returns:
        List[Dict[str, Any]]: Список найденных вакансий
    """
    vacancies = get_all_vacancies()
    keyword_lower = keyword.lower()

    found = []
    for vacancy in vacancies:
        title = vacancy.get('name', '').lower()
        if keyword_lower in title:
            found.append({
                "id": vacancy.get('id'),
                "name": vacancy.get('name'),
                "company": vacancy.get('employer', {}).get('name'),
                "url": vacancy.get('alternate_url')
            })

    return found


def filter_vacancies_by_company(company_name: str) -> List[Dict[str, Any]]:
    """Фильтрует вакансии по названию компании."""
    vacancies = get_all_vacancies()
    company_lower = company_name.lower()

    return [
        v for v in vacancies
        if v.get('employer', {}).get('name', '').lower() == company_lower
    ]