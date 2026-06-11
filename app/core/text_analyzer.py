"""
Модуль для анализа текста вакансий.
Выполняет очистку, токенизацию, лемматизацию и извлечение KM-функций.
"""
import re
import nltk
from typing import List, Dict, Any, Tuple
from collections import Counter

# Скачиваем необходимые данные NLTK (требуется один раз)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)  # для новых версий nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy3

# Инициализация морфологического анализатора для русского языка
morph = pymorphy3.MorphAnalyzer()

# Русские стоп-слова
RUSSIAN_STOPWORDS = set(stopwords.words('russian'))

# Дополнительный список стоп-слов
EXTRA_STOPWORDS = {
    'работа', 'вакансия', 'компания', 'сотрудник', 'должность',
    'требование', 'обязанность', 'условие', 'опыт', 'год', 'месяц',
    'будет', 'также', 'более', 'менее', 'нужно', 'может', 'быть',
    'hr', 'hh', 'руб', 'рублей', 'москва', 'спб', 'санкт-петербург', 'российский',
    'наш', 'ваш', 'который', 'это', 'этот', 'эта', 'эти',
    'quot', 'и', 'в', 'на', 'с', 'по', 'к', 'у', 'о', 'об',
    'для', 'без', 'до', 'за', 'через', 'между', 'перед',
    'the', 'and', 'for', 'our', 'with', 'are', 'is', 'of', 'to',
    'a', 'an', 'in', 'that', 'it', 'we', 'you', 'they', 'be',
    'am', 'at', 'by', 'on', 'as', 'or', 'but', 'not', 'so',
    'team', 'looking', 'join', 'work', 'job', 'position'
}
STOPWORDS = RUSSIAN_STOPWORDS.union(EXTRA_STOPWORDS)

# Словарь функций управления знаниями (KM) с ключевыми словами
KM_FUNCTIONS_DICT = {
    "База знаний": [
        "база знаний", "базу знаний", "базой знаний", "базе знаний",
        "knowledge base", "репозиторий знаний", "база данных знаний"
    ],
    "Документация": [
        "документация", "документацию", "документацией", "документации",
        "техническая документация", "технической документации",
        "руководство пользователя", "пользовательская документация",
        "api документация"
    ],
    "Обучение": [
        "обучение", "обучения", "обучению", "обучением",
        "тренинг", "тренинги", "онбординг", "адаптация",
        "наставничество", "тьюторство", "менторство"
    ],
    "Процессы": [
        "описание процессов", "описание бизнес-процессов",
        "бизнес-процесс", "реинжиниринг", "регламент",
        "стандартизация", "bpmn", "process management"
    ],
    "Коммуникации": [
        "обмен знаниями", "knowledge sharing", "коммуникация",
        "внутренние коммуникации", "сообщество практик",
        "community of practice", "лучшие практики"
    ],
    "Аналитика": [
        "аналитика", "анализ данных", "data analysis",
        "метрики", "kpi", "отчетность", "дашборд"
    ]
}


class TextAnalyzer:
    """Анализатор текста вакансий."""

    def __init__(self):
        self.morph = morph
        self.stopwords = STOPWORDS

    def clean_text(self, text: str) -> str:
        """
        Очистка текста: удаление HTML-тегов, спецсимволов, лишних пробелов.
        """
        if not text:
            return ""

        # Удаление HTML-тегов
        text = re.sub(r'<[^>]+>', ' ', text)
        # Удаление спецсимволов
        text = re.sub(r'[^a-zA-Zа-яА-ЯёЁ0-9\s]', ' ', text)
        # Приведение к нижнему регистру
        text = text.lower()
        # Удаление лишних пробелов
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def lemmatize(self, word: str) -> str:
        """
        Лемматизация одного слова (приведение к начальной форме).
        """
        if not word or len(word) < 2:
            return word
        parsed = self.morph.parse(word)[0]
        return parsed.normal_form

    def tokenize_and_lemmatize(self, text: str) -> List[str]:
        """
        Токенизация и лемматизация текста.
        Возвращает список лемм (слов в начальной форме).
        """
        if not text:
            return []

        # Токенизация
        tokens = word_tokenize(text, language='russian')

        # Лемматизация и фильтрация
        lemmas = []
        for token in tokens:
            # Пропускаем стоп-слова
            if token in self.stopwords:
                continue
            # Пропускаем короткие слова (длиной 1-2 символа)
            if len(token) <= 2:
                continue
            # Пропускаем числа
            if token.isdigit():
                continue

            lemma = self.lemmatize(token)
            lemmas.append(lemma)

        return lemmas

    def extract_km_functions(self, text: str) -> Dict[str, Any]:
        """
        Извлечение функций управления знаниями из текста.

        Returns:
            Dict с ключами:
            - functions: список найденных функций
            - score: оценка насыщенности KM (0-1)
            - details: детальная информация по каждой функции
        """
        if not text:
            return {"functions": [], "score": 0, "details": {}}

        text_lower = text.lower()
        found_functions = {}

        for func_name, keywords in KM_FUNCTIONS_DICT.items():
            found_keywords = []
            for kw in keywords:
                if kw.lower() in text_lower:
                    found_keywords.append(kw)

            if found_keywords:
                found_functions[func_name] = found_keywords

        # Расчет скора: процент найденных функций
        total_functions = len(KM_FUNCTIONS_DICT)
        found_count = len(found_functions)
        score = found_count / total_functions if total_functions > 0 else 0

        return {
            "functions": list(found_functions.keys()),
            "score": round(score, 3),
            "details": found_functions
        }

    def get_term_frequencies(self, lemmas: List[str], top_n: int = 20) -> List[Tuple[str, int]]:
        """
        Расчет частотности терминов.

        Returns:
            Список кортежей (термин, частота) в порядке убывания
        """
        if not lemmas:
            return []

        freq = Counter(lemmas)
        return freq.most_common(top_n)

    def analyze_vacancy_text(self, requirement: str, responsibility: str) -> Dict[str, Any]:
        """
        Полный анализ текста вакансии.
        Объединяет все этапы обработки.
        """
        # Объединяем требования и обязанности
        full_text = f"{requirement or ''} {responsibility or ''}".strip()

        if not full_text:
            return {
                "has_text": False,
                "functions": [],
                "score": 0,
                "top_terms": [],
                "message": "Нет текста для анализа"
            }

        # Очистка
        cleaned = self.clean_text(full_text)

        # Токенизация и лемматизация
        lemmas = self.tokenize_and_lemmatize(cleaned)

        # Извлечение KM-функций
        km_result = self.extract_km_functions(cleaned)

        # Топ терминов
        top_terms = self.get_term_frequencies(lemmas, top_n=10)

        return {
            "has_text": True,
            "functions": km_result["functions"],
            "score": km_result["score"],
            "top_terms": [{"word": word, "count": count} for word, count in top_terms],
            "total_lemmas": len(lemmas)
        }


# Создание глобального экземпляра
text_analyzer = TextAnalyzer()


def analyze_vacancy_text(requirement: str, responsibility: str) -> Dict[str, Any]:
    """
    Упрощенная функция для анализа текста вакансии.
    """
    return text_analyzer.analyze_vacancy_text(requirement, responsibility)