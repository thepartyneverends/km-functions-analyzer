async function loadSalaryStats() {
            const container = document.getElementById('salary-stats');
            try {
                const data = await App.fetchAPI('/stats/salary');
                if (data) {
                    const fromMin = data.salary_from_min?.toLocaleString() || '—';
                    const fromMax = data.salary_from_max?.toLocaleString() || '—';
                    const fromAvg = data.salary_from_avg?.toLocaleString() || '—';
                    const toMin = data.salary_to_min?.toLocaleString() || '—';
                    const toMax = data.salary_to_max?.toLocaleString() || '—';
                    const toAvg = data.salary_to_avg?.toLocaleString() || '—';

                    container.innerHTML = `
                        <div class="salary-row">
                            <span class="salary-label">📊 Зарплата "от" (мин)</span>
                            <span class="salary-value">${fromMin} ₽</span>
                        </div>
                        <div class="salary-row">
                            <span class="salary-label">📊 Зарплата "от" (макс)</span>
                            <span class="salary-value">${fromMax} ₽</span>
                        </div>
                        <div class="salary-row">
                            <span class="salary-label">📊 Зарплата "от" (средняя)</span>
                            <span class="salary-value">${fromAvg} ₽</span>
                        </div>
                        <div class="salary-row">
                            <span class="salary-label">🎯 Зарплата "до" (мин)</span>
                            <span class="salary-value">${toMin} ₽</span>
                        </div>
                        <div class="salary-row">
                            <span class="salary-label">🎯 Зарплата "до" (макс)</span>
                            <span class="salary-value">${toMax} ₽</span>
                        </div>
                        <div class="salary-row">
                            <span class="salary-label">🎯 Зарплата "до" (средняя)</span>
                            <span class="salary-value">${toAvg} ₽</span>
                        </div>
                    `;
                } else {
                    container.innerHTML = '<div class="empty-state">❌ Нет данных по зарплатам</div>';
                }
            } catch (error) {
                console.error('Ошибка загрузки зарплатной статистики:', error);
                container.innerHTML = '<div class="empty-state">❌ Ошибка загрузки данных</div>';
            }
        }

        async function loadCompaniesStats() {
            const container = document.getElementById('companies-stats');
            try {
                const data = await App.fetchAPI('/stats/companies');
                if (data && data.companies && data.companies.length > 0) {
                    const companiesHtml = data.companies.slice(0, 10).map((c, idx) => `
                        <div class="list-item">
                            <span class="item-name">${idx + 1}. ${c.name}</span>
                            <span class="item-count">${c.vacancies_count} ваканс.</span>
                        </div>
                    `).join('');
                    container.innerHTML = companiesHtml;
                } else {
                    container.innerHTML = '<div class="empty-state">📭 Нет данных о компаниях</div>';
                }
            } catch (error) {
                console.error('Ошибка загрузки компаний:', error);
                container.innerHTML = '<div class="empty-state">❌ Ошибка загрузки данных</div>';
            }
        }

        async function loadSkillsStats() {
            const container = document.getElementById('skills-stats');
            try {
                const data = await App.fetchAPI('/skills/top?limit=10');
                if (data && data.top_skills && data.top_skills.length > 0) {
                    const skillsHtml = data.top_skills.map((s, idx) => `
                        <div class="list-item">
                            <span class="item-name">${idx + 1}. ${s.skill}</span>
                            <span class="item-count">${s.count} раз</span>
                        </div>
                    `).join('');
                    container.innerHTML = skillsHtml;
                } else {
                    container.innerHTML = '<div class="empty-state">📭 Нет данных о навыках</div>';
                }
            } catch (error) {
                console.error('Ошибка загрузки навыков:', error);
                container.innerHTML = '<div class="empty-state">❌ Ошибка загрузки данных</div>';
            }
        }

        loadSalaryStats();
        loadCompaniesStats();
        loadSkillsStats();