"""
входные сериализаторы точек
"""

from pydantic import BaseModel, Field


class OrganizationByRadiusInput(BaseModel):
    """
    параметры поиска организаций в радиусе
    """
    lat: float = Field(..., description="Широта центральной точки")
    lon: float = Field(..., description="Долгота центральной точки")
    radius: float = Field(..., description="Радиус в метрах")


class OrganizationByRectangleInput(BaseModel):
    """
    Параметры поиска организаций в прямоугольнике
    """
    lat_min: float = Field(..., description="Минимальная широта")
    lat_max: float = Field(..., description="Максимальная широта")
    lon_min: float = Field(..., description="Минимальная долгота")
    lon_max: float = Field(..., description="Максимальная долгота")


class OrganizationSearchInput(BaseModel):
    """
    параметры поиска организаций по названию
    """
    name: str = Field(..., description="Название организации для поиска")
