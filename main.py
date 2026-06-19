import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.config import API_TITLE, API_DESCRIPTION, API_VERSION, API_V1_PREFIX, HOST, PORT, RELOAD
from app.api.routers import vacancies, stats, skills, search, km_analysis, text_analysis, clustering

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)

# Подключение роутеров API
app.include_router(vacancies.router, prefix=API_V1_PREFIX)
app.include_router(stats.router, prefix=API_V1_PREFIX)
app.include_router(skills.router, prefix=API_V1_PREFIX)
app.include_router(search.router, prefix=API_V1_PREFIX)
app.include_router(km_analysis.router, prefix=API_V1_PREFIX)
app.include_router(text_analysis.router, prefix=API_V1_PREFIX)
app.include_router(clustering.router, prefix=API_V1_PREFIX)

# Статические файлы (CSS, JS, страницы)
static_dir = Path(__file__).parent / "app" / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    app.mount("/pages", StaticFiles(directory=str(static_dir / "pages")), name="pages")


@app.get("/", response_class=FileResponse, include_in_schema=False)
async def root():
    return FileResponse(static_dir / "pages" / "index.html")


@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok", "service": API_TITLE}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=RELOAD,
        log_level="info"
    )