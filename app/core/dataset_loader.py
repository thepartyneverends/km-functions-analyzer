"""
Загрузчик данных из CSV-датасета HH.ru
Адаптирован под структуру: id, name, employer_name, area_name, salary_from/to, description, key_skills и т.д.
"""
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from app.config import DATA_DIR

# Путь к датасету (укажите правильное имя файла!)
DATASET_PATH = DATA_DIR / "vacancies_2020.csv"  # Замените на ваше имя файла


def load_dataset() -> pd.DataFrame:
    """Загружает CSV-датасет в Pandas DataFrame."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Датасет не найден: {DATASET_PATH}")

    df = pd.read_csv(DATASET_PATH, encoding='utf-8')
    print(f"✅ Загружено {len(df)} записей из датасета")
    print(f"📋 Колонки: {list(df.columns)}")
    return df


def parse_key_skills(key_skills_value) -> List[Dict[str, str]]:
    """
    Преобразует key_skills из строки в список словарей.

    Формат в датасете может быть:
    - "Python, SQL, Git"
    - "[{'name': 'Python'}, {'name': 'SQL'}]"
    - NaN или пустая строка
    """
    if pd.isna(key_skills_value):
        return []

    skills_str = str(key_skills_value)

    # Если строка пустая
    if not skills_str or skills_str == 'nan':
        return []

    # Если это JSON-подобная строка со списком словарей
    if skills_str.strip().startswith('[') and "'name'" in skills_str:
        try:
            # Заменяем одинарные кавычки на двойные для JSON
            import ast
            skills_list = ast.literal_eval(skills_str)
            if isinstance(skills_list, list):
                return [{'name': s.get('name', '')} for s in skills_list if s.get('name')]
        except:
            pass

    # Если это строка с разделителями
    if ',' in skills_str:
        return [{'name': s.strip()} for s in skills_str.split(',') if s.strip()]

    # Если это просто одно значение
    return [{'name': skills_str}]


def parse_specializations(spec_value) -> List[str]:
    """Преобразует specializations в читаемый список."""
    if pd.isna(spec_value):
        return []

    spec_str = str(spec_value)
    if spec_str.strip().startswith('['):
        try:
            import ast
            spec_list = ast.literal_eval(spec_str)
            if isinstance(spec_list, list):
                return [s.get('name', str(s)) if isinstance(s, dict) else str(s) for s in spec_list]
        except:
            pass

    return [spec_str] if spec_str and spec_str != 'nan' else []


def parse_employer_industries(industries_value) -> List[str]:
    """Преобразует employer_industries в список."""
    if pd.isna(industries_value):
        return []

    ind_str = str(industries_value)
    if ind_str.strip().startswith('['):
        try:
            import ast
            ind_list = ast.literal_eval(ind_str)
            if isinstance(ind_list, list):
                return [i.get('name', str(i)) if isinstance(i, dict) else str(i) for i in ind_list]
        except:
            pass

    return [ind_str] if ind_str and ind_str != 'nan' else []


def convert_to_vacancy_format(df: pd.DataFrame, limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Преобразует DataFrame в формат, ожидаемый API приложения.

    Args:
        df: DataFrame с данными из датасета
        limit: ограничить количество записей (для тестирования)
    """
    vacancies = []

    # Ограничиваем количество, если нужно
    df_to_process = df.head(limit) if limit else df

    for idx, row in df_to_process.iterrows():
        # Пропускаем записи без названия
        name = row.get('name', '')
        if pd.isna(name) or not str(name).strip():
            continue

        # Формируем описание из поля description
        description = row.get('description', '')
        if pd.isna(description):
            description = ''

        # Разделяем описание на требования и обязанности (если есть структура)
        # В HH обычно requirements и responsibilities в одном поле
        requirement = str(description)[:2000] if description else ''
        responsibility = ''

        # Извлекаем зарплату
        salary = None
        salary_from = row.get('salary_from')
        salary_to = row.get('salary_to')
        salary_currency = row.get('salary_currency', 'RUR')

        if (pd.notna(salary_from) and salary_from) or (pd.notna(salary_to) and salary_to):
            salary = {
                'from': int(salary_from) if pd.notna(salary_from) and salary_from else None,
                'to': int(salary_to) if pd.notna(salary_to) and salary_to else None,
                'currency': salary_currency if pd.notna(salary_currency) else 'RUR',
                'gross': bool(row.get('salary_gross')) if pd.notna(row.get('salary_gross')) else False
            }

        # Собираем вакансию в нужном формате
        vacancy = {
            'id': str(row.get('id', f'mock_{idx}')),
            'name': str(name),
            'employer': {
                'id': str(row.get('employer_id', '')),
                'name': str(row.get('employer_name', '')) if pd.notna(row.get('employer_name')) else ''
            },
            'area': {
                'id': str(row.get('area_id', '')),
                'name': str(row.get('area_name', '')) if pd.notna(row.get('area_name')) else ''
            },
            'salary': salary,
            'published_at': str(row.get('published_at', '')),
            'alternate_url': str(row.get('alternate_url', '')) if pd.notna(row.get('alternate_url')) else '',
            'url': str(row.get('alternate_url', '')) if pd.notna(row.get('alternate_url')) else '',
            'snippet': {
                'requirement': requirement[:500] if requirement else '',
                'responsibility': responsibility[:500] if responsibility else ''
            },
            'key_skills': parse_key_skills(row.get('key_skills')),
            'experience': {
                'id': str(row.get('experience_id', '')),
                'name': str(row.get('experience_name', '')) if pd.notna(row.get('experience_name')) else ''
            },
            'employment': {
                'id': str(row.get('employment_id', '')),
                'name': str(row.get('employment_name', '')) if pd.notna(row.get('employment_name')) else ''
            },
            'schedule': {
                'id': str(row.get('schedule_id', '')),
                'name': str(row.get('schedule_name', '')) if pd.notna(row.get('schedule_name')) else ''
            },
            'specializations': parse_specializations(row.get('specializations')),
            'employer_industries': parse_employer_industries(row.get('employer_industries')),
            'address': {
                'city': str(row.get('address_city', '')) if pd.notna(row.get('address_city')) else '',
                'street': str(row.get('address_street', '')) if pd.notna(row.get('address_street')) else ''
            } if pd.notna(row.get('address_city')) or pd.notna(row.get('address_street')) else None,
            'archived': bool(row.get('archived', False)) if pd.notna(row.get('archived')) else False,
            'premium': bool(row.get('premium', False)) if pd.notna(row.get('premium')) else False
        }

        vacancies.append(vacancy)

    print(f"✅ Конвертировано {len(vacancies)} вакансий в нужный формат")
    return vacancies


def save_to_mock_json(vacancies: List[Dict], output_path: Path = DATA_DIR / "mock_hh_response.json"):
    """Сохраняет конвертированные данные в формате, который использует data_loader.py."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Формат, который ожидает data_loader.py
    output_data = {
        'items': vacancies,
        'found': len(vacancies),
        'pages': 1,
        'per_page': len(vacancies),
        'page': 0,
        'clusters': None,
        'arguments': None,
        'alternate_url': ''
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, default=str)

    print(f"✅ Данные сохранены в {output_path}")
    print(f"📊 Всего сохранено вакансий: {len(vacancies)}")


def get_dataset_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Возвращает информацию о датасете."""
    return {
        'total_rows': len(df),
        'columns': list(df.columns),
        'date_range': {
            'min': str(df['published_at'].min()) if 'published_at' in df.columns else None,
            'max': str(df['published_at'].max()) if 'published_at' in df.columns else None
        },
        'vacancies_with_salary': int(df['salary_from'].notna().sum()) if 'salary_from' in df.columns else 0,
        'unique_employers': int(df['employer_name'].nunique()) if 'employer_name' in df.columns else 0,
        'unique_areas': int(df['area_name'].nunique()) if 'area_name' in df.columns else 0
    }


# Для быстрого тестирования
if __name__ == "__main__":
    print("🚀 Тестирование загрузчика датасета...")

    # Загружаем данные
    df = load_dataset()

    # Выводим информацию
    info = get_dataset_info(df)
    print(f"\n📊 Информация о датасете:")
    print(f"   - Всего записей: {info['total_rows']}")
    print(f"   - Уникальных работодателей: {info['unique_employers']}")
    print(f"   - Уникальных регионов: {info['unique_areas']}")
    print(f"   - Вакансий с зарплатой: {info['vacancies_with_salary']}")

    # Конвертируем первые 1000 записей для теста
    vacancies = convert_to_vacancy_format(df, limit=1000)

    # Сохраняем
    save_to_mock_json(vacancies)

    print("\n🎉 Готово! Теперь можно запускать приложение.")