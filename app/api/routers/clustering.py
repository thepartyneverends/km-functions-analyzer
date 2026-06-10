"""
Роутер для эндпоинтов кластеризации.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any

from app.core.clustering import clusterer, run_clustering, get_clustered_vacancies

router = APIRouter(prefix="/clustering", tags=["Кластеризация"])


@router.post("/run")
async def perform_clustering(
        n_clusters: int = Query(4, ge=2, le=10, description="Количество кластеров")
):
    """
    Запустить кластеризацию вакансий.
    """
    result = run_clustering(n_clusters=n_clusters)

    if not result['success']:
        raise HTTPException(status_code=400, detail=result.get('error', 'Ошибка кластеризации'))

    return result


@router.get("/vacancies")
async def get_clustered_vacancies_list():
    """
    Получить список вакансий с присвоенными кластерами.
    """
    return {
        'success': True,
        'vacancies': get_clustered_vacancies()
    }


@router.get("/info/{cluster_id}")
async def get_cluster_info(cluster_id: int):
    """
    Получить информацию о конкретном кластере.
    """
    if not clusterer.is_fitted:
        run_clustering()

    info = clusterer.get_cluster_info(cluster_id)

    if info.get('size', 0) == 0:
        raise HTTPException(status_code=404, detail=f"Кластер {cluster_id} не найден или пуст")

    return info


@router.get("/visualization")
async def get_clustering_visualization():
    """
    Получить данные для визуализации кластеров (2D координаты).
    """
    if not clusterer.is_fitted:
        run_clustering()

    coords = clusterer.get_pca_coordinates()

    if not coords:
        raise HTTPException(status_code=400, detail="Нет данных для визуализации")

    return coords


@router.post("/predict")
async def predict_cluster_for_text(text: str = Query(..., description="Текст вакансии для анализа")):
    """
    Предсказать кластер для произвольного текста вакансии.
    """
    if not clusterer.is_fitted:
        run_clustering()

    try:
        prediction = clusterer.predict(text)
        return {
            'success': True,
            'prediction': prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))