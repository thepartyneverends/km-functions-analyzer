from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Настройка браузера
driver = webdriver.Chrome()  # должен быть установлен ChromeDriver

# Открытие страницы поиска
search_url = 'https://hh.ru/search/vacancy?text=управление+знаниями&area=113'
driver.get(search_url)

# Небольшая пауза для загрузки страницы
time.sleep(3)

# Поиск элементов с вакансиями
vacancy_cards = driver.find_elements(By.CSS_SELECTOR, '[data-qa="serp-item__title"]')

for card in vacancy_cards[:10]:  # первые 10 вакансий
    print(card.text)
    print(card.get_attribute('href'))

driver.quit()