// Загрузка общей (показательной) статистики
        async function loadBatchStats() {
            try {
                const data = await App.fetchAPI('/text-analysis/batch?limit=200');
                if (data) {
                    document.getElementById('totalAnalyzed').textContent = data.total_analyzed || 0;
                    document.getElementById('vacanciesWithKm').textContent = data.vacancies_with_km || 0;
                    document.getElementById('avgKmScore').textContent = Math.round((data.average_km_score || 0) * 100);
                }
            } catch (error) {
                console.error('Ошибка загрузки статистики:', error);
            }
        }

        // Загрузка топ терминов и количества уникальных терминов
        async function loadTopTerms() {
            try {
                const data = await App.fetchAPI('/text-analysis/top-terms?limit=30');
                if (data && data.top_terms) {
                    document.getElementById('uniqueTerms').textContent = data.total_unique_terms || 0;

                    const termsHtml = data.top_terms.map(t =>
                        `<span class="cloud-term" title="Встречается ${t.count} раз">${t.word}<span style="font-size: 0.7rem; opacity: 0.7;"> (${t.count})</span></span>`
                    ).join('');
                    document.getElementById('topTermsCloud').innerHTML = termsHtml || '<p style="color: #adb5bd;">Нет данных</p>';
                }
            } catch (error) {
                console.error('Ошибка загрузки терминов:', error);
                document.getElementById('topTermsCloud').innerHTML = '<p style="color: #e74c3c;">❌ Ошибка загрузки</p>';
            }
        }

        // Анализ конкретной вакансии по ID
        async function analyzeVacancy() {
            const vacancyId = document.getElementById('vacancyId').value.trim();
            const container = document.getElementById('single-analysis');

            if (!vacancyId) {
                container.innerHTML = `
                    <div class="analysis-result analysis-error">
                        ❌ Введите ID вакансии
                    </div>
                `;
                return;
            }

            container.innerHTML = '<div class="analysis-result">🔄 Анализ текста вакансии... (NLTK + pymorphy2)</div>';

            try {
                const result = await App.fetchAPI(`/text-analysis/vacancy/${vacancyId}`);

                if (result && result.analysis && result.analysis.has_text) {
                    const analysis = result.analysis;
                    const score = analysis.score;
                    let scoreClass = 'score-low';
                    let scoreText = 'Низкая';
                    if (score >= 0.5) {
                        scoreClass = 'score-high';
                        scoreText = 'Высокая';
                    } else if (score >= 0.2) {
                        scoreClass = 'score-medium';
                        scoreText = 'Средняя';
                    }

                    container.innerHTML = `
                        <div class="analysis-result analysis-success">
                            <h3>📄 ${result.title || 'Без названия'}</h3>
                            <p><strong>🏢 Компания:</strong> ${result.employer || 'Не указана'}</p>
                            <p><strong>📊 Всего лемм в тексте:</strong> ${analysis.total_lemmas || 0}</p>
                            <p><strong>🏆 Топ терминов:</strong></p>
                            <div class="term-list">
                                ${analysis.top_terms.map(t => `<span class="term-item">${t.word}<span class="term-count">(${t.count})</span></span>`).join('')}
                            </div>
                        </div>
                    `;
                } else {
                    container.innerHTML = `
                        <div class="analysis-result analysis-error">
                            ❌ Вакансия с ID "${vacancyId}" не найдена или не содержит текста для анализа
                        </div>
                    `;
                }
            } catch (error) {
                console.error('Ошибка анализа:', error);
                container.innerHTML = `
                    <div class="analysis-result analysis-error">
                        ❌ Ошибка при анализе вакансии
                    </div>
                `;
            }
        }

        loadBatchStats();
        loadTopTerms();