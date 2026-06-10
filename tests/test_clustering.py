# check_km_distribution.py
import sys
sys.path.insert(0, '.')

from app.core.data_loader import get_vacancies
from app.core.text_analyzer import text_analyzer

vacancies = get_vacancies()
print(f"Всего вакансий: {len(vacancies)}")

scores = []
for v in vacancies:
    snippet = v.get('snippet', {})
    text = f"{snippet.get('requirement', '')} {snippet.get('responsibility', '')}"
    result = text_analyzer.analyze_vacancy_text(text, '')
    scores.append(result['score'])

print(f"Средний KM Score: {sum(scores)/len(scores):.2f}")
print(f"Вакансий с score > 0: {sum(1 for s in scores if s > 0)}")
print(f"Вакансий с score = 0: {sum(1 for s in scores if s == 0)}")