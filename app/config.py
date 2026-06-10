"""
Настройки и конфигурации приложения.
"""
from pathlib import Path
from typing import Optional

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "mock_hh_response.json"

# Настройки API
API_V1_PREFIX = "/api/v1"
API_TITLE = "KM Jobs Analyzer API"
API_DESCRIPTION = """
API для анализа вакансий с функциями управления знаниями.

## Возможности:
- Получение списка вакансий с пагинацией
- Поиск вакансий по ID и ключевым словам
- Статистика по вакансиям, компаниям, навыкам
- Топ ключевых навыков
"""
API_VERSION = "1.0.0"

# Настройки пагинации
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Настройки сервера
HOST = "127.0.0.1"
PORT = 8000
RELOAD = True

# Кеширование
CACHE_ENABLED = True