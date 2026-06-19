# Модуль анализа текста вакансий на КМ-функции
from typing import List, Dict, Any

# Словарь функций KM с ключевыми словами для поиска
KM_FUNCTIONS = {
    "KM-1: База знаний": ["база знаний", "knowledge base", "базой знаний", "репозиторий знаний"],
    "KM-2: Документация": ["документация", "documentation", "техническая документация", "руководство пользователя"],
    "KM-3: Обучение": ["обучение", "training", "онбординг", "onboarding", "адаптация"],
    "KM-4: Процессы": ["описание процессов", "business process", "реинжиниринг", "стандартизация"],
    "KM-5: Коммуникации": ["обмен знаниями", "knowledge sharing", "внутренние коммуникации", "сообщество"]
}

# Анализирует текст и возвращает найденные KM-функции
def analyze_km_functions(text: str) -> Dict[str, Any]:
    if not text:
        return {"functions": [], "score": 0}

    text_lower = text.lower()
    found = []

    for func_name, keywords in KM_FUNCTIONS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.append(func_name)
                break

    return {
        "functions": list(set(found)),  # уникальные функции
        "count": len(set(found)),
        "score": len(set(found)) / len(KM_FUNCTIONS)  # 0-1
    }