"""
Модуль для кластеризации вакансий на основе текстового анализа.
Группирует похожие должности по функциям управления знаниями.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import joblib
from pathlib import Path

from app.core.data_loader import get_vacancies
from app.core.text_analyzer import text_analyzer


class VacancyClusterer:
    """
    Кластеризатор вакансий.
    Преобразует тексты вакансий в векторы и группирует их в кластеры.
    """

    def __init__(self, n_clusters: int = 5, random_state: int = 42):
        """
        Инициализация кластеризатора.

        Args:
            n_clusters: количество кластеров (будет подобрано автоматически, если None)
            random_state: для воспроизводимости результатов
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.vectorizer = None
        self.kmeans = None
        self.is_fitted = False
        self.silhouette_avg = 0

    def prepare_texts(self, min_km_score: float = 0.1) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Подготовка текстов для векторизации.

        Args:
            min_km_score: минимальный KM Score для включения вакансии (по умолчанию 0.1)
        """
        vacancies = get_vacancies()
        texts = []
        metadata = []

        for vacancy in vacancies:
            snippet = vacancy.get('snippet', {})
            requirement = snippet.get('requirement', '') or ''
            responsibility = snippet.get('responsibility', '') or ''
            raw_text = f"{requirement} {responsibility}".strip()

            if not raw_text or len(raw_text) < 50:
                continue

            # ★★★ НОВОЕ: проверяем KM Score ★★★
            from app.core.text_analyzer import analyze_vacancy_text
            analysis = analyze_vacancy_text(requirement, responsibility)

            if analysis['score'] < min_km_score:
                continue  # Пропускаем вакансии с низким KM Score

            # Очищаем и лемматизируем
            cleaned = text_analyzer.clean_text(raw_text)
            lemmas = text_analyzer.tokenize_and_lemmatize(cleaned)

            processed_text = ' '.join(lemmas)

            if processed_text and len(processed_text) > 20:
                texts.append(processed_text)
                metadata.append({
                    'id': vacancy.get('id'),
                    'title': vacancy.get('name'),
                    'employer': vacancy.get('employer', {}).get('name'),
                    'km_score': analysis['score']
                })

        print(f"✅ Отобрано {len(texts)} вакансий с KM Score >= {min_km_score}")
        return texts, metadata

    def vectorize(self, texts: List[str]) -> np.ndarray:
        """
        Векторизация текстов с помощью TF-IDF.

        Args:
            texts: список обработанных текстов

        Returns:
            np.ndarray: матрица признаков
        """
        self.vectorizer = TfidfVectorizer(
            max_features=500,  # Ограничиваем количество признаков
            min_df=2,  # Термин должен встречаться минимум в 2 документах
            max_df=0.8,  # Игнорируем термины, встречающиеся более чем в 80% документов
            ngram_range=(1, 2)  # Учитываем отдельные слова и биграммы
        )

        X = self.vectorizer.fit_transform(texts)
        print(f"✅ Векторизация завершена: {X.shape[0]} документов, {X.shape[1]} признаков")
        return X

    def find_optimal_clusters(self, X: np.ndarray, max_clusters: int = 10) -> Dict[str, Any]:
        """
        Поиск оптимального количества кластеров методом "локтя" и силуэта.

        Args:
            X: матрица признаков
            max_clusters: максимальное количество кластеров для проверки

        Returns:
            Dict с метриками и рекомендованным числом кластеров
        """
        inertias = []
        silhouette_scores = []

        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X, kmeans.labels_))

        # Находим "локоть" (точку максимального изгиба)
        deltas = np.diff(inertias)
        delta2_deltas = np.diff(deltas)
        elbow = np.argmax(delta2_deltas) + 2

        # Оптимальное по силуэту
        best_silhouette = np.argmax(silhouette_scores) + 2

        return {
            'k_range': list(range(2, max_clusters + 1)),
            'inertias': inertias,
            'silhouette_scores': silhouette_scores,
            'elbow_k': elbow,
            'best_silhouette_k': best_silhouette,
            'recommended_k': best_silhouette
        }

    def fit(self, texts: List[str], n_clusters: int = None) -> Dict[str, Any]:
        """
        Обучает модель кластеризации.

        Args:
            texts: список текстов
            n_clusters: количество кластеров (если None, используется self.n_clusters)

        Returns:
            Dict с результатами обучения
        """
        if n_clusters:
            self.n_clusters = n_clusters

        # Векторизация
        X = self.vectorize(texts)

        # Обучение KMeans
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=self.random_state,
            n_init=10,
            max_iter=300
        )
        self.labels = self.kmeans.fit_predict(X)

        # Оценка качества
        if len(set(self.labels)) > 1:
            self.silhouette_avg = silhouette_score(X, self.labels)

        self.is_fitted = True
        self.X = X

        # Получаем топ-термины для каждого кластера
        self.cluster_top_terms = self._get_cluster_top_terms()

        return {
            'n_clusters': self.n_clusters,
            'silhouette_score': round(self.silhouette_avg, 3),
            'cluster_sizes': self._get_cluster_sizes(),
            'cluster_top_terms': self.cluster_top_terms
        }

    def _get_cluster_sizes(self) -> Dict[int, int]:
        """Возвращает размер каждого кластера."""
        sizes = {}
        for label in set(self.labels):
            sizes[int(label)] = int(np.sum(self.labels == label))
        return sizes

    def _get_cluster_top_terms(self, top_n: int = 10) -> Dict[int, List[Tuple[str, float]]]:
        """
        Возвращает топ-термины для каждого кластера.
        """
        if not self.is_fitted:
            return {}

        feature_names = self.vectorizer.get_feature_names_out()
        centroids = self.kmeans.cluster_centers_

        cluster_terms = {}
        for cluster_idx in range(self.n_clusters):
            # Получаем веса терминов для центроида кластера
            centroid = centroids[cluster_idx]
            # Находим индексы топ-терминов
            top_indices = centroid.argsort()[-top_n:][::-1]
            top_terms = [(feature_names[i], round(centroid[i], 3)) for i in top_indices]
            cluster_terms[cluster_idx] = top_terms

        return cluster_terms

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Предсказывает кластер для нового текста.

        Args:
            text: текст вакансии

        Returns:
            Dict с предсказанием и дистанциями
        """
        if not self.is_fitted:
            raise ValueError("Модель не обучена. Сначала вызовите fit()")

        # Обработка текста
        cleaned = text_analyzer.clean_text(text)
        lemmas = text_analyzer.tokenize_and_lemmatize(cleaned)
        processed = ' '.join(lemmas)

        # Векторизация
        X_new = self.vectorizer.transform([processed])

        # Предсказание
        cluster = int(self.kmeans.predict(X_new)[0])
        distances = self.kmeans.transform(X_new)[0].tolist()

        return {
            'cluster': cluster,
            'distances': distances,
            'top_terms': self.cluster_top_terms.get(cluster, [])
        }

    def get_cluster_info(self, cluster_id: int) -> Dict[str, Any]:
        """
        Получает информацию о конкретном кластере.
        """
        if not self.is_fitted:
            return {}

        return {
            'cluster_id': cluster_id,
            'size': self._get_cluster_sizes().get(cluster_id, 0),
            'top_terms': self.cluster_top_terms.get(cluster_id, []),
            'silhouette_score': self.silhouette_avg
        }

    def assign_clusters_to_vacancies(self) -> List[Dict[str, Any]]:
        """
        Присваивает кластеры всем вакансиям и возвращает обогащенный список.
        """
        if not self.is_fitted:
            return []

        vacancies = get_vacancies()
        results = []

        for i, vacancy in enumerate(vacancies[:len(self.labels)]):
            results.append({
                'id': vacancy.get('id'),
                'title': vacancy.get('name'),
                'employer': vacancy.get('employer', {}).get('name'),
                'cluster': int(self.labels[i]),
                'cluster_top_terms': self.cluster_top_terms.get(int(self.labels[i]), [])[:5]
            })

        return results

    def get_pca_coordinates(self) -> Dict[str, List]:
        """
        Получает 2D координаты для визуализации кластеров (PCA).
        """
        if not self.is_fitted:
            return {}

        pca = PCA(n_components=2, random_state=self.random_state)
        coords = pca.fit_transform(self.X.toarray())

        return {
            'x': coords[:, 0].tolist(),
            'y': coords[:, 1].tolist(),
            'labels': self.labels.tolist(),
            'explained_variance': pca.explained_variance_ratio_.tolist()
        }

    def save_model(self, path: str = 'models/clustering_model.joblib'):
        """
        Сохраняет обученную модель в файл.
        """
        if not self.is_fitted:
            raise ValueError("Модель не обучена")

        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump({
            'vectorizer': self.vectorizer,
            'kmeans': self.kmeans,
            'n_clusters': self.n_clusters,
            'silhouette_score': self.silhouette_avg,
            'cluster_top_terms': self.cluster_top_terms
        }, save_path)

        print(f"✅ Модель сохранена в {save_path}")

    def load_model(self, path: str = 'models/clustering_model.joblib'):
        """
        Загружает обученную модель из файла.
        """
        load_path = Path(path)
        if not load_path.exists():
            raise FileNotFoundError(f"Файл модели {path} не найден")

        data = joblib.load(load_path)
        self.vectorizer = data['vectorizer']
        self.kmeans = data['kmeans']
        self.n_clusters = data['n_clusters']
        self.silhouette_avg = data['silhouette_score']
        self.cluster_top_terms = data['cluster_top_terms']
        self.is_fitted = True

        print(f"✅ Модель загружена из {path}")


# Создание глобального экземпляра
clusterer = VacancyClusterer(n_clusters=4)


def run_clustering(n_clusters: int = 4) -> Dict[str, Any]:
    """
    Запускает полный процесс кластеризации.
    """
    # Подготовка текстов
    texts, metadata = clusterer.prepare_texts()

    if len(texts) < n_clusters:
        return {
            'success': False,
            'error': f'Недостаточно данных для кластеризации: {len(texts)} текстов, требуется минимум {n_clusters}'
        }

    # Обучение
    result = clusterer.fit(texts, n_clusters=n_clusters)

    # Получение координат для визуализации
    pca_coords = clusterer.get_pca_coordinates()

    return {
        'success': True,
        'n_clusters': result['n_clusters'],
        'silhouette_score': result['silhouette_score'],
        'cluster_sizes': result['cluster_sizes'],
        'cluster_top_terms': result['cluster_top_terms'],
        'total_vacancies_analyzed': len(texts),
        'pca_coordinates': pca_coords
    }


def get_clustered_vacancies() -> List[Dict[str, Any]]:
    """
    Возвращает список вакансий с присвоенными кластерами.
    """
    if not clusterer.is_fitted:
        # Автоматически запускаем кластеризацию с параметрами по умолчанию
        texts, _ = clusterer.prepare_texts()
        if len(texts) >= 4:
            clusterer.fit(texts, n_clusters=4)

    return clusterer.assign_clusters_to_vacancies()