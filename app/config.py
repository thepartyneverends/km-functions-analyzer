from pathlib import Path
from typing import Optional
import os

from dotenv import load_dotenv

load_dotenv()

HH_CLIENT_ID = os.getenv('HH_CLIENT_ID')
HH_CLIENT_SECRET = os.getenv('HH_CLIENT_SECRET')

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "hh_km_vacancies.json"

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