from fastapi import APIRouter, HTTPException
from app.core.data_loader import get_vacancies
from app.core.km_analyzer import analyze_km_functions
from app.core.text_analyzer import analyze_vacancy_text

router = APIRouter(prefix="/km-analysis", tags=["KM анализ"])


@router.get("/vacancy/{vacancy_id}")
async def analyze_vacancy(vacancy_id: str):
    """Анализирует конкретную вакансию на наличие функций KM."""
    vacancies = get_vacancies()
    vacancy = next((v for v in vacancies if v.get('id') == vacancy_id), None)

    if not vacancy:
        raise HTTPException(404, "Вакансия не найдена")

    # Берем текст из требований и обязанностей
    snippet = vacancy.get('snippet', {})
    text = f"{snippet.get('requirement', '')} {snippet.get('responsibility', '')}"

    analysis = analyze_km_functions(text)
    return {"vacancy_id": vacancy_id, "title": vacancy.get('name'), **analysis}


@router.get("/statistics")
async def get_km_statistics():
    """
    Статистика по всем вакансиям: какие функции KM встречаются чаще всего.
    """
    from collections import Counter

    vacancies = get_vacancies()
    all_functions = []
    vacancies_with_km_count = 0
    all_scores = []

    for vac in vacancies:
        snippet = vac.get('snippet', {})
        text = f"{snippet.get('requirement', '')} {snippet.get('responsibility', '')}"

        # Анализируем текст
        result = analyze_vacancy_text(text, '')

        # Собираем функции
        all_functions.extend(result['functions'])

        # Считаем score
        all_scores.append(result['score'])

        # Считаем вакансии с score > 0
        if result['score'] > 0:
            vacancies_with_km_count += 1

    # Статистика по функциям
    stats = Counter(all_functions)

    # Средний score
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    return {
        "total_vacancies": len(vacancies),
        "vacancies_with_km": vacancies_with_km_count,  # ← ТОЛЬКО score > 0
        "vacancies_without_km": len(vacancies) - vacancies_with_km_count,  # ← добавили для наглядности
        "average_km_score": round(avg_score, 3),
        "function_distribution": dict(stats)
    }