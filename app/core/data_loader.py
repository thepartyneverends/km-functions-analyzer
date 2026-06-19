# Модуль для загрузки и управления данными о вакансиях
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from functools import lru_cache

from app.config import BASE_DIR

DATA_FILE = BASE_DIR / 'data' / 'hh_km_vacancies.json'


class DataLoader:

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path or DATA_FILE
        self._cache: Optional[List[Dict[str, Any]]] = None

        if not self.file_path.exists():
            print(f"Файл не найден.")

    # Загрузчик данных из JSON файла
    def load(self) -> List[Dict[str, Any]]:
        if self._cache is not None:
            return self._cache

        if not self.file_path.exists():
            print(f"Файл не найден!")
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Поддержка разных форматов JSON
            if isinstance(data, list):
                vacancies = data
            elif isinstance(data, dict) and 'items' in data:
                vacancies = data.get('items', [])
            else:
                vacancies = []

            print(f"Загружено {len(vacancies)} вакансий из JSON файла")
            self._cache = vacancies
            return vacancies

        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
            return []
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return []

    def clear_cache(self):
        self._cache = None
        print("Кэш данных очищен")

    def refresh(self):
        self.clear_cache()
        return self.load()

    def get_vacancy_by_id(self, vacancy_id: str) -> Optional[Dict[str, Any]]:

        vacancies = self.load()
        for vacancy in vacancies:
            if str(vacancy.get('id')) == str(vacancy_id):
                return vacancy
        return None

data_loader = DataLoader()


@lru_cache(maxsize=1)
def get_vacancies() -> List[Dict[str, Any]]:
    return data_loader.load()


def refresh_vacancies_cache():
    data_loader.clear_cache()
    get_vacancies.cache_clear()
    return get_vacancies()