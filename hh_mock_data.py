# hh_mock_data.py

import json
from pathlib import Path

def fetch_vacancies_mock(query: str = "управление знаниями"):
    """Возвращает имитацию ответа API HH.ru для разработки."""
    # Путь к этому файлу с JSON
    data_file = Path(__file__).parent / "mock_hh_response.json"
    with open(data_file, 'r', encoding='utf-8') as f:
        full_response = json.load(f)
    return full_response['items']

def fetch_vacancies_real(query: str):
    """Заглушка: здесь был бы реальный запрос к API."""
    # Для диплома можно оставить этот комментарий:
    # Из-за блокировки IP (ошибка 403) используем тестовые данные.
    return fetch_vacancies_mock(query)