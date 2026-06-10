"""
Роутер для эндпоинтов анализа текста.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any

from app.core.data_loader import get_vacancies
from app.core.text_analyzer import text_analyzer, analyze_vacancy_text

router = APIRouter(prefix="/text-analysis", tags=["Анализ текста"])


@router.get("/vacancy/{vacancy_id}")
async def analyze_vacancy_text_endpoint(vacancy_id: str):
    """
    Анализ текста конкретной вакансии на наличие KM-функций.
    """
    vacancies = get_vacancies()
    vacancy = next((v for v in vacancies if v.get('id') == vacancy_id), None)

    if not vacancy:
        raise HTTPException(status_code=404, detail="Вакансия не найдена")

    snippet = vacancy.get('snippet', {})
    requirement = snippet.get('requirement', '')
    responsibility = snippet.get('responsibility', '')

    analysis = analyze_vacancy_text(requirement, responsibility)

    return {
        "vacancy_id": vacancy_id,
        "title": vacancy.get('name'),
        "employer": vacancy.get('employer', {}).get('name'),
        "analysis": analysis
    }


@router.get("/batch")
async def analyze_batch_vacancies(
        limit: int = Query(10, ge=1, le=50, description="Количество вакансий для анализа")
):
    """
    Пакетный анализ нескольких вакансий.
    """
    vacancies = get_vacancies()
    results = []

    for vacancy in vacancies[:limit]:
        snippet = vacancy.get('snippet', {})
        analysis = analyze_vacancy_text(
            snippet.get('requirement', ''),
            snippet.get('responsibility', '')
        )

        results.append({
            "id": vacancy.get('id'),
            "title": vacancy.get('name'),
            "employer": vacancy.get('employer', {}).get('name'),
            "km_functions": analysis["functions"],
            "km_score": analysis["score"],
            "has_text": analysis["has_text"]
        })

    # Статистика по выборке
    avg_score = sum(r["km_score"] for r in results) / len(results) if results else 0
    vacancies_with_km = sum(1 for r in results if r["km_score"] > 0)

    return {
        "total_analyzed": len(results),
        "vacancies_with_km": vacancies_with_km,
        "average_km_score": round(avg_score, 3),
        "results": results
    }


@router.get("/top-terms")
async def get_top_terms_across_vacancies(
        limit: int = Query(20, ge=1, le=50, description="Количество топ-терминов")
):
    """
    Топ терминов, встречающихся во всех вакансиях.
    """
    from collections import Counter

    vacancies = get_vacancies()
    all_lemmas = []

    for vacancy in vacancies:
        snippet = vacancy.get('snippet', {})
        text = f"{snippet.get('requirement', '')} {snippet.get('responsibility', '')}"
        cleaned = text_analyzer.clean_text(text)
        lemmas = text_analyzer.tokenize_and_lemmatize(cleaned)
        all_lemmas.extend(lemmas)

    freq = Counter(all_lemmas)
    top_terms = freq.most_common(limit)

    return {
        "total_unique_terms": len(freq),
        "total_term_occurrences": len(all_lemmas),
        "top_terms": [{"word": word, "count": count} for word, count in top_terms]
    }