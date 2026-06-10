import requests
from time import sleep

session = requests.Session()
# Мой заголовок, чтобы API понимало, кто к нему стучится
session.headers.update({
    'User-Agent': 'KM-functions-diplom/1.0 (contact: ustimenkosergey05@yandex.ru)'
})

# 2. Параметры запроса
url = 'https://api.hh.ru/vacancies'
params = {
    'text': 'программист',
    'area': 2,  # Россия
    'per_page': 10,  # Количество на странице
    'page': 0  # Номер страницы
}

print(f"Отправляю запрос: {params}")
# 3. Выполнение запроса
response = session.get(url, params=params)

# 4. Обработка результата
if response.status_code == 200:
    print("Успех!")
    data = response.json()
    print(f"Всего найдено вакансий: {data['found']}")
    print("Первые 5 найденных вакансий:")
    for item in data['items'][:5]:
        print(f" - {item['name']}")
else:
    print(f"Ошибка! Статус: {response.status_code}")
    print("Ответ сервера:", response.text)

# Небольшая пауза перед следующим запросом, если он будет
sleep(0.5)