"""
Модели данных для вакансий (Pydantic).
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class Employer(BaseModel):
    """Модель работодателя."""
    id: Optional[str] = None
    name: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "9876",
                "name": "Росатом"
            }
        }


class Area(BaseModel):
    """Модель региона."""
    id: Optional[str] = None
    name: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "113",
                "name": "Россия"
            }
        }


class Salary(BaseModel):
    """Модель зарплаты."""
    from_: Optional[int] = Field(None, alias="from", description="Нижняя граница")
    to: Optional[int] = None
    currency: Optional[str] = None
    gross: Optional[bool] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "from": 150000,
                "to": 200000,
                "currency": "RUR",
                "gross": True
            }
        }


class Snippet(BaseModel):
    """Модель краткого описания (сниппета)."""
    requirement: Optional[str] = Field(None, description="Требования")
    responsibility: Optional[str] = Field(None, description="Обязанности")

    class Config:
        json_schema_extra = {
            "example": {
                "requirement": "Опыт внедрения KM систем от 2-х лет",
                "responsibility": "Разработка стратегии управления знаниями"
            }
        }


class KeySkill(BaseModel):
    """Модель ключевого навыка."""
    name: str

    class Config:
        json_schema_extra = {
            "example": {"name": "Управление знаниями"}
        }


class Vacancy(BaseModel):
    """Модель вакансии."""
    id: str
    name: str
    employer: Optional[Employer] = None
    area: Optional[Area] = None
    salary: Optional[Salary] = None
    published_at: Optional[str] = None
    url: Optional[str] = None
    alternate_url: Optional[str] = None
    snippet: Optional[Snippet] = None
    key_skills: Optional[List[KeySkill]] = []

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "78901234",
                "name": "Специалист по управлению знаниями",
                "employer": {"id": "9876", "name": "Росатом"},
                "area": {"id": "113", "name": "Россия"},
                "salary": {"from": 150000, "to": 200000, "currency": "RUR", "gross": True}
            }
        }