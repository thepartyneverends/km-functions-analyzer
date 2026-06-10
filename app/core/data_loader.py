"""
Загрузка данных из JSON-файла.
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from functools import lru_cache

from app.config import DATA_FILE


class DataLoader:
    """Загрузчик данных из JSON-файла."""

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or DATA_FILE
        self._cache: Optional[List[Dict[str, Any]]] = None

    def load(self) -> List[Dict[str, Any]]:
        """
        Загружает данные из JSON-файла.

        Returns:
            List[Dict[str, Any]]: Список вакансий
        """
        if self._cache is not None:
            return self._cache

        if not self.file_path.exists():
            print(f"❌ Файл {self.file_path} не найден!")
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                full_response = json.load(f)

            vacancies = full_response.get('items', [])
            print(f"✅ Загружено {len(vacancies)} вакансий из {self.file_path}")
            self._cache = vacancies
            return vacancies

        except json.JSONDecodeError as e:
            print(f"❌ Ошибка парсинга JSON: {e}")
            return []
        except Exception as e:
            print(f"❌ Непредвиденная ошибка: {e}")
            return []

    def clear_cache(self):
        """Очищает кеш данных."""
        self._cache = None
        print("🔄 Кеш данных очищен")


# Глобальный экземпляр загрузчика
data_loader = DataLoader()


@lru_cache(maxsize=1)
def get_vacancies() -> List[Dict[str, Any]]:
    """
    Возвращает список всех вакансий (с кешированием).
    """
    return data_loader.load()


def refresh_vacancies_cache():
    """Обновляет кеш вакансий."""
    data_loader.clear_cache()
    get_vacancies.cache_clear()