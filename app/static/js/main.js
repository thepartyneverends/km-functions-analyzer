// app/static/js/main.js
// Общие функции для всего приложения

// Базовый URL API
const API_BASE = '/api/v1';

// Функция загрузки данных с API
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

// Функция отображения уведомлений
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Форматирование даты
function formatDate(dateString) {
    if (!dateString) return 'Не указана';
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
}

// Форматирование зарплаты
function formatSalary(salary) {
    if (!salary) return 'Не указана';
    const from = salary.from ? `от ${salary.from.toLocaleString()}` : '';
    const to = salary.to ? `до ${salary.to.toLocaleString()}` : '';
    const currency = salary.currency || 'RUB';

    if (from && to) return `${from} ${to} ${currency}`;
    if (from) return `${from} ${currency}`;
    if (to) return `${to} ${currency}`;
    return 'Не указана';
}

// Экспорт функций для использования в других скриптах
window.App = {
    API_BASE,
    fetchAPI,
    showToast,
    formatDate,
    formatSalary
};