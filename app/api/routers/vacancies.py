from fastapi import APIRouter, Query
from app.core.data_loader import get_vacancies

router = APIRouter(prefix="/vacancies", tags=["Вакансии"])

@router.get("/")
async def get_vacancies_list(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    vacancies = get_vacancies()
    total = len(vacancies)
    paginated = vacancies[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "vacancies": paginated
    }


@router.get("/debug")
async def debug_vacancies():
    from app.core.data_loader import data_loader
    vacancies = data_loader.load()
    return {
        "total": len(vacancies),
        "first_5": vacancies[:5] if vacancies else [],
        "file_exists": data_loader.file_path.exists(),
        "file_path": str(data_loader.file_path)
    }