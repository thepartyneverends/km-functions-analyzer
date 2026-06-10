#!/usr/bin/env python
"""
Скрипт для конвертации CSV-датасета в формат приложения.
Запустите один раз: python convert_dataset.py
"""
import sys
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent))

from app.core.dataset_loader import load_dataset, convert_to_vacancy_format, save_to_mock_json, get_dataset_info
from app.config import DATA_DIR


def main():
    print("=" * 60)
    print("🚀 КОНВЕРТАЦИЯ ДАТАСЕТА HH.RU ДЛЯ FASTAPI")
    print("=" * 60)

    # 1. Загружаем сырой датасет
    print("\n📂 Загрузка датасета...")
    df = load_dataset()

    # 2. Информация о датасете
    info = get_dataset_info(df)
    print(f"\n📊 Информация о датасете:")
    print(f"   - Всего записей: {info['total_rows']}")
    print(f"   - Уникальных работодателей: {info['unique_employers']}")
    print(f"   - Уникальных регионов: {info['unique_areas']}")
    print(f"   - Вакансий с зарплатой: {info['vacancies_with_salary']}")

    # 3. Спрашиваем, сколько записей обработать
    print("\n💡 Рекомендация: Для начала возьмите 5000 записей, потом добавите больше")
    try:
        limit_input = input("Сколько записей обработать? (Enter = все, укажите число): ").strip()
        if limit_input:
            limit = int(limit_input)
        else:
            limit = None
    except:
        limit = None

    # 4. Конвертируем
    print(f"\n🔄 Конвертация вакансий...")
    vacancies = convert_to_vacancy_format(df, limit=limit)

    # 5. Сохраняем
    print(f"\n💾 Сохранение в mock_hh_response.json...")
    save_to_mock_json(vacancies, DATA_DIR / "mock_hh_response.json")

    # 6. Краткий итог
    print("\n" + "=" * 60)
    print("✅ ГОТОВО!")
    print("=" * 60)
    print("\nТеперь вы можете запустить приложение:")
    print("   python run.py")
    print("\nИ открыть в браузере:")
    print("   http://127.0.0.1:8000")


if __name__ == "__main__":
    main()