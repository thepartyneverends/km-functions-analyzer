"""
Быстрый тест для проверки работы анализатора текста.
Запустите: python test_text_analyzer.py
"""
import sys
import os

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.text_analyzer import text_analyzer

# Тестовые тексты вакансий
test_cases = [
    {
        "name": "KM-специалист",
        "requirement": "Опыт внедрения систем управления знаниями от 3 лет. Знание методологий KM.",
        "responsibility": "Создание и ведение базы знаний компании. Организация обмена опытом между сотрудниками. Проведение обучения."
    },
    {
        "name": "Технический писатель",
        "requirement": "Умение писать техническую документацию. Опыт работы с Confluence.",
        "responsibility": "Создание руководств пользователя. Ведение базы знаний техподдержки."
    },
    {
        "name": "Обычный разработчик",
        "requirement": "Знание Python, Django, SQL. Опыт разработки от 2 лет.",
        "responsibility": "Написание кода, ревью, участие в ежедневных митингах."
    }
]

print("=" * 70)
print("🔬 ТЕСТ АНАЛИЗАТОРА ТЕКСТА ВАКАНСИЙ")
print("=" * 70)

for test in test_cases:
    print(f"\n📌 Тестируем вакансию: {test['name']}")
    print("-" * 50)

    # Анализируем текст
    result = text_analyzer.analyze_vacancy_text(
        requirement=test['requirement'],
        responsibility=test['responsibility']
    )

    print(f"📄 Есть текст для анализа: {'✅ Да' if result['has_text'] else '❌ Нет'}")
    print(f"🎯 Функции KM: {', '.join(result['functions']) if result['functions'] else '❌ Не найдены'}")
    print(f"📊 KM Score: {result['score'] * 100:.1f}%")
    print(f"📝 Количество лемм: {result['total_lemmas']}")

    if result['top_terms']:
        terms_str = ", ".join([f"{t['word']}({t['count']})" for t in result['top_terms'][:5]])
        print(f"🏆 Топ термины: {terms_str}")
    else:
        print("🏆 Топ термины: не найдены")

print("\n" + "=" * 70)
print("✅ Тест завершен!")
print("=" * 70)