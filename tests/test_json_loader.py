import json
from pathlib import Path


def load_vacancies_from_json(file_path: str = "hh_km_vacancies.json"):
    """
    Загружает вакансии из JSON-файла.

    Args:
        file_path: путь к JSON-файлу с данными вакансий

    Returns:
        list: список вакансий
    """
    # Определяем путь к файлу
    data_file = Path(__file__).parent / file_path

    # Проверяем, существует ли файл
    if not data_file.exists():
        print(f"❌ Файл {file_path} не найден!")
        print(f"   Ищем по пути: {data_file.absolute()}")
        return []

    # Загружаем данные из JSON
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            full_response = json.load(f)

        # Извлекаем список вакансий (ключ 'items' в ответе API HH)
        vacancies = full_response.get('items', [])
        print(f"Успешно загружено {len(vacancies)} вакансий из файла {file_path}")
        return vacancies

    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {e}")
        return []
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")
        return []


def print_vacancies_to_console(vacancies):
    """
    Выводит информацию о вакансиях в консоль в читаемом формате.

    Args:
        vacancies: список вакансий
    """
    if not vacancies:
        print("Нет данных для отображения")
        return

    print("\n" + "=" * 80)
    print(f"📊 ОТЧЕТ ПО ВАКАНСИЯМ (всего: {len(vacancies)})")
    print("=" * 80)

    for idx, vacancy in enumerate(vacancies, 1):
        print(f"\n--- Вакансия №{idx} ---")
        print(f"📌 Название: {vacancy.get('name', 'Не указано')}")
        print(f"🏢 Компания: {vacancy.get('employer', {}).get('name', 'Не указана')}")
        print(f"📍 Регион: {vacancy.get('area', {}).get('name', 'Не указан')}")

        # Зарплата
        salary = vacancy.get('salary')
        if salary:
            salary_from = salary.get('from', 'не указана')
            salary_to = salary.get('to', 'не указана')
            currency = salary.get('currency', '')
            print(f"💰 Зарплата: от {salary_from} до {salary_to} {currency}")
        else:
            print(f"💰 Зарплата: не указана")

        # Ключевые навыки
        key_skills = vacancy.get('key_skills', [])
        if key_skills:
            skills_names = [skill.get('name', '') for skill in key_skills if skill.get('name')]
            print(f"🔧 Ключевые навыки: {', '.join(skills_names)}")
        else:
            print(f"🔧 Ключевые навыки: не указаны")

        # Требования и обязанности (сниппеты)
        snippet = vacancy.get('snippet', {})
        requirement = snippet.get('requirement', '')
        responsibility = snippet.get('responsibility', '')

        if requirement:
            print(f"📋 Требования: {requirement[:150]}..." if len(requirement) > 150 else f"📋 Требования: {requirement}")
        if responsibility:
            print(f"📝 Обязанности: {responsibility[:150]}..." if len(
                responsibility) > 150 else f"📝 Обязанности: {responsibility}")

        # Ссылка на вакансию
        url = vacancy.get('alternate_url', '')
        if url:
            print(f"🔗 Ссылка: {url}")

    print("\n" + "=" * 80)
    print("🏁 Конец отчета")
    print("=" * 80)


def print_vacancies_as_table(vacancies):
    """
    Выводит вакансии в виде простой таблицы.
    """
    if not vacancies:
        print("Нет данных для отображения")
        return

    print("\n📋 КРАТКАЯ ТАБЛИЦА ВАКАНСИЙ")
    print("-" * 80)
    print(f"{'№':<3} {'Название вакансии':<35} {'Компания':<25} {'Зарплата':<15}")
    print("-" * 80)

    for idx, vacancy in enumerate(vacancies, 1):
        name = vacancy.get('name', '---')[:33] + '..' if len(vacancy.get('name', '')) > 35 else vacancy.get('name',
                                                                                                            '---')
        company = vacancy.get('employer', {}).get('name', '---')[:23] + '..' if len(
            vacancy.get('employer', {}).get('name', '')) > 25 else vacancy.get('employer', {}).get('name', '---')

        salary = vacancy.get('salary')
        if salary and salary.get('from'):
            salary_str = f"от {salary.get('from')}"
        elif salary and salary.get('to'):
            salary_str = f"до {salary.get('to')}"
        else:
            salary_str = "не указана"

        print(f"{idx:<3} {name:<35} {company:<25} {salary_str:<15}")

    print("-" * 80)


if __name__ == "__main__":
    print("🚀 Запуск тестового загрузчика вакансий...")

    # Загружаем вакансии из JSON-файла
    vacancies = load_vacancies_from_json("../data/hh_km_vacancies.json")

    if vacancies:
        # Вариант 1: Подробный вывод в консоль
        print_vacancies_to_console(vacancies)

        # Вариант 2: Краткая таблица (раскомментируйте, если нужна)
        # print_vacancies_as_table(vacancies)

        # Дополнительно: простая статистика
        print("\n📈 Простая статистика:")
        print(f"   - Всего вакансий: {len(vacancies)}")
        print(f"   - Вакансий с указанной зарплатой: {sum(1 for v in vacancies if v.get('salary'))}")
        print(
            f"   - Уникальных компаний: {len(set(v.get('employer', {}).get('name') for v in vacancies if v.get('employer', {}).get('name')))}")

        # Вывод списка всех названий вакансий
        print("\n📝 Список всех вакансий:")
        for idx, vacancy in enumerate(vacancies, 1):
            print(f"   {idx}. {vacancy.get('name', 'Без названия')}")
    else:
        print(
            "❌ Не удалось загрузить данные")