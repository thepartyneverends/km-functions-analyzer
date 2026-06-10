"""
Расчет статистик по вакансиям.
"""
from typing import List, Dict, Any
from app.core.data_loader import get_vacancies


def calculate_total_stats() -> Dict[str, Any]:
    """Рассчитывает общую статистику по всем вакансиям."""
    vacancies = get_vacancies()

    if not vacancies:
        return {
            "total_vacancies": 0,
            "vacancies_with_salary": 0,
            "vacancies_without_salary": 0,
            "unique_companies": 0,
            "salary_percentage": 0.0
        }

    # Подсчет вакансий с зарплатой
    with_salary = 0
    for v in vacancies:
        salary = v.get('salary')
        if salary and salary.get('from'):
            with_salary += 1

    # Уникальные компании
    unique_companies = len(set(
        v.get('employer', {}).get('name')
        for v in vacancies
        if v.get('employer', {}).get('name')
    ))

    total = len(vacancies)
    salary_percentage = round(with_salary / total * 100, 1) if total > 0 else 0.0

    return {
        "total_vacancies": total,
        "vacancies_with_salary": with_salary,
        "vacancies_without_salary": total - with_salary,
        "unique_companies": unique_companies,
        "salary_percentage": salary_percentage
    }


def calculate_companies_stats() -> Dict[str, Any]:
    """Рассчитывает статистику по компаниям."""
    vacancies = get_vacancies()

    if not vacancies:
        return {"total_companies": 0, "companies": []}

    companies_stats = {}
    for vacancy in vacancies:
        company_name = vacancy.get('employer', {}).get('name')
        if company_name:
            companies_stats[company_name] = companies_stats.get(company_name, 0) + 1

    # Сортируем по убыванию
    sorted_companies = sorted(companies_stats.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_companies": len(companies_stats),
        "companies": [{"name": name, "vacancies_count": count} for name, count in sorted_companies]
    }


def calculate_top_skills(limit: int = 10) -> Dict[str, Any]:
    """Рассчитывает топ наиболее часто встречающихся навыков."""
    vacancies = get_vacancies()

    if not vacancies:
        return {"total_unique_skills": 0, "top_skills": []}

    skills_count = {}
    for vacancy in vacancies:
        for skill in vacancy.get('key_skills', []):
            skill_name = skill.get('name')
            if skill_name:
                skills_count[skill_name] = skills_count.get(skill_name, 0) + 1

    sorted_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)[:limit]

    return {
        "total_unique_skills": len(skills_count),
        "top_skills": [{"skill": name, "count": count} for name, count in sorted_skills]
    }


def calculate_salary_stats() -> Dict[str, Any]:
    """Рассчитывает статистику по зарплатам."""
    vacancies = get_vacancies()

    salaries_from = []
    salaries_to = []

    for vacancy in vacancies:
        salary = vacancy.get('salary')
        if salary:
            if salary.get('from'):
                salaries_from.append(salary.get('from'))
            if salary.get('to'):
                salaries_to.append(salary.get('to'))

    return {
        "salary_from_min": min(salaries_from) if salaries_from else None,
        "salary_from_max": max(salaries_from) if salaries_from else None,
        "salary_from_avg": round(sum(salaries_from) / len(salaries_from), 0) if salaries_from else None,
        "salary_to_min": min(salaries_to) if salaries_to else None,
        "salary_to_max": max(salaries_to) if salaries_to else None,
        "salary_to_avg": round(sum(salaries_to) / len(salaries_to), 0) if salaries_to else None,
        "sample_size": len(salaries_from)
    }