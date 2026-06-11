async function fetchAPI(endpoint) {
            try {
                const response = await fetch(`/api/v1${endpoint}`);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                return null;
            }
        }

        async function loadKMStatistics() {
            try {
                const data = await fetchAPI('/km-analysis/statistics');
                if (data) {
                    const distribution = data.function_distribution || {};
                    const container = document.getElementById('function-distribution');

                    if (Object.keys(distribution).length > 0) {
                        container.innerHTML = Object.entries(distribution).map(([func, count]) => `
                            <div class="function-item">
                                <span class="function-name">${func}</span>
                                <span class="function-count">${count} вакансий</span>
                            </div>
                        `).join('');
                    } else {
                        container.innerHTML = '<p style="color: #6c757d;">Нет данных</p>';
                    }

                    document.getElementById('km-summary').innerHTML = `
                        <strong>📈 Всего вакансий в выборке:</strong> ${data.total_vacancies || 0}<br>
                        <strong>🎯 Вакансий с функциями KM:</strong> ${data.vacancies_with_km || 0}
                    `;
                }
            } catch (error) {
                console.error('Ошибка:', error);
            }
        }

        async function analyzeVacancy() {
            const vacancyId = document.getElementById('vacancyId').value.trim();
            const container = document.getElementById('vacancy-analysis');

            if (!vacancyId) {
                container.innerHTML = `<div class="analysis-result analysis-error">❌ Введите ID вакансии</div>`;
                return;
            }

            container.innerHTML = '<div class="analysis-result">🔄 Анализ вакансии...</div>';

            try {
                const result = await fetchAPI(`/km-analysis/vacancy/${vacancyId}`);

                // Проверяем, есть ли ошибка
                if (result && result.detail) {
                    container.innerHTML = `<div class="analysis-result analysis-error">❌ Вакансия с ID "${vacancyId}" не найдена</div>`;
                    return;
                }

                // Проверяем, что получили данные
                if (result && result.title) {
                    const scorePercent = Math.round((result.score || 0) * 100);
                    let scoreEmoji = '🟢';
                    let scoreText = 'Низкая';
                    if (scorePercent >= 50) {
                        scoreEmoji = '🔴';
                        scoreText = 'Высокая';
                    } else if (scorePercent >= 20) {
                        scoreEmoji = '🟡';
                        scoreText = 'Средняя';
                    }

                    container.innerHTML = `
                        <div class="analysis-result analysis-success">
                            <h3>📄 ${result.title || 'Без названия'}</h3>
                            <p><strong>🏢 Компания:</strong> ${result.employer || 'Не указана'}</p>
                            <p><strong>🎯 Степень релевантности KM:</strong> ${scorePercent}% ${scoreEmoji} (${scoreText})</p>
                            <p><strong>🔧 Обнаруженные функции:</strong> ${result.functions?.length > 0 ? result.functions.map(f => `<span class="function-badge">${f}</span>`).join('') : 'Не найдены'}</p>
                        </div>
                    `;
                } else {
                    container.innerHTML = `<div class="analysis-result analysis-error">❌ Не удалось проанализировать вакансию</div>`;
                }
            } catch (error) {
                console.error('Ошибка:', error);
                container.innerHTML = `<div class="analysis-result analysis-error">❌ Ошибка запроса: ${error.message}</div>`;
            }
        }

        loadKMStatistics();