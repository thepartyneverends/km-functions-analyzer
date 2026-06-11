async function runClustering() {
            const btn = document.getElementById('runClusteringBtn');
            const statusDiv = document.getElementById('clusteringStatus');
            const statsDiv = document.getElementById('clusterStats');

            btn.disabled = true;
            btn.textContent = '⏳ ВЫПОЛНЯЕТСЯ...';
            statusDiv.innerHTML = `
                <div class="status-card">
                    🔄 Кластеризация запущена. Это может занять 10-30 секунд...
                </div>
            `;
            statsDiv.style.display = 'none';

            try {
                const response = await fetch('/api/v1/clustering/run?n_clusters=4', { method: 'POST' });
                const data = await response.json();

                if (data.success) {
                    statusDiv.innerHTML = `
                        <div class="status-card" style="border-left-color: #27ae60; background: #e8f8f0;">
                            ✅ Кластеризация успешно завершена!
                        </div>
                    `;

                    // Статистика
                    displayStats(data.n_clusters, data.silhouette_score, data.total_vacancies_analyzed);

                    // Визуализация
                    await loadVisualization();

                    // Карточки кластеров
                    displayClusterInfo(data.cluster_top_terms, data.cluster_sizes);

                    statsDiv.style.display = 'block';
                } else {
                    statusDiv.innerHTML = `
                        <div class="status-card" style="border-left-color: #e74c3c; background: #fee;">
                            ❌ Ошибка: ${data.error || 'Неизвестная ошибка'}
                        </div>
                    `;
                }
            } catch (error) {
                statusDiv.innerHTML = `
                    <div class="status-card" style="border-left-color: #e74c3c; background: #fee;">
                        ❌ Ошибка при выполнении кластеризации: ${error.message}
                    </div>
                `;
            } finally {
                btn.disabled = false;
                btn.textContent = '🚀 ЗАПУСТИТЬ КЛАСТЕРИЗАЦИЮ';
            }
        }

        function displayStats(nClusters, silhouetteScore, totalVacancies) {
            const container = document.getElementById('statsBoxes');
            container.innerHTML = `
                <div class="stat-box">
                    <div class="stat-number">${nClusters}</div>
                    <div class="stat-label">КЛАСТЕРОВ</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">${silhouetteScore}</div>
                    <div class="stat-label">SILHOUETTE SCORE</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">${totalVacancies}</div>
                    <div class="stat-label">ВАКАНСИЙ</div>
                </div>
            `;
        }

        async function loadVisualization() {
            try {
                const response = await fetch('/api/v1/clustering/visualization');
                const data = await response.json();

                if (data.x && data.y) {
                    const trace = {
                        x: data.x,
                        y: data.y,
                        mode: 'markers',
                        type: 'scatter',
                        text: data.labels.map(l => `Кластер ${l}`),
                        marker: {
                            size: 10,
                            color: data.labels,
                            colorscale: 'Viridis',
                            showscale: true,
                            colorbar: { title: 'Кластер' }
                        }
                    };

                    const layout = {
                        title: '',
                        xaxis: { title: 'Первая главная компонента', gridcolor: '#e9ecef' },
                        yaxis: { title: 'Вторая главная компонента', gridcolor: '#e9ecef' },
                        hovermode: 'closest',
                        height: 450,
                        plot_bgcolor: '#f8f9fa',
                        paper_bgcolor: '#f8f9fa'
                    };

                    Plotly.newPlot('scatterPlot', [trace], layout, { responsive: true });
                }
            } catch (error) {
                console.error('Ошибка загрузки визуализации:', error);
                document.getElementById('scatterPlot').innerHTML = '<p style="color: #e74c3c;">❌ Не удалось загрузить визуализацию</p>';
            }
        }

        function displayClusterInfo(clusterTerms, clusterSizes) {
            const colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'];
            const clusterNames = [
                'Техническая документация и разработка',
                'Управление проектами и процессы',
                'IT и аналитика',
                'Обучение и HR',
                'Дополнительный кластер'
            ];

            const container = document.getElementById('clustersInfo');

            container.innerHTML = Object.entries(clusterTerms).map(([cluster, terms]) => `
                <div class="cluster-card cluster-${cluster % 5}">
                    <h4>📌 КЛАСТЕР ${cluster}</h4>
                    <div class="cluster-size">${clusterSizes[cluster]} вакансий</div>
                    <p style="margin: 10px 0; font-size: 0.85rem;"><strong>Предполагаемая сфера:</strong> ${clusterNames[cluster % 5]}</p>
                    <p style="margin: 10px 0 5px 0;"><strong>🏆 Ключевые термины:</strong></p>
                    <div class="terms-list">
                        ${terms.slice(0, 12).map(term => `
                            <span class="term-badge">${term[0]}<span class="term-weight">(${term[1]})</span></span>
                        `).join('')}
                    </div>
                </div>
            `).join('');
        }

        // Автоматический запуск при загрузке
        document.addEventListener('DOMContentLoaded', () => {
            runClustering();
        });