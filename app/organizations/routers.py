from fastapi import APIRouter, Depends, HTTPException
from pyfa_converter_v2 import QueryDepends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.dependencies import verify_api_key
from app.organizations.input_serializators import (
    OrganizationByRadiusInput,
    OrganizationByRectangleInput,
    OrganizationSearchInput,
)
from app.organizations.schemas import BuildingSchema, OrganizationDetailSchema, OrganizationWithBuildingSchema, OrganizationSchema
from app.organizations.services import BuildingService, OrganizationService

router = APIRouter(prefix="/api", dependencies=[Depends(verify_api_key)])


@router.get("/organizations/by-building/{building_id}", response_model=list[OrganizationWithBuildingSchema])
async def get_organizations_by_building(
    building_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Список всех организаций находящихся в конкретном здании с координатами
    """
    orgs = await OrganizationService.get_by_building(building_id, session)
    return orgs


@router.get("/organizations/by-activity/{activity_id}", response_model=list[OrganizationSchema])
async def get_organizations_by_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    список всех организаций, которые относятся к указанному виду деятельности.
    Включает организации из всех дочерних активностей.
    """
    orgs = await OrganizationService.get_by_activity(activity_id, session)
    return orgs


@router.get("/organizations/by-radius", response_model=list[OrganizationSchema])
async def get_organizations_by_radius(
    filters: OrganizationByRadiusInput = QueryDepends(OrganizationByRadiusInput),
    session: AsyncSession = Depends(get_session)
):
    """
    список организаций в заданном радиусе от точки
    """
    orgs = await OrganizationService.get_by_radius(filters.lat, filters.lon, filters.radius, session)
    return orgs


@router.get("/organizations/by-rectangle", response_model=list[OrganizationSchema])
async def get_organizations_by_rectangle(
    filters: OrganizationByRectangleInput = QueryDepends(OrganizationByRectangleInput),
    session: AsyncSession = Depends(get_session)
):
    """
    Список организаций в прямоугольной области
    """
    orgs = await OrganizationService.get_by_rectangle(
        filters.lat_min, filters.lat_max, filters.lon_min, filters.lon_max, session
    )
    return orgs


@router.get("/organizations/search", response_model=list[OrganizationSchema])
async def search_organizations(
    filters: OrganizationSearchInput = QueryDepends(OrganizationSearchInput),
    session: AsyncSession = Depends(get_session)
):
    """
    Поиск организации по названию
    """
    orgs = await OrganizationService.search_by_name(filters.name, session)
    return orgs


@router.get("/organizations/{org_id}", response_model=OrganizationDetailSchema)
async def get_organization_by_id(
    org_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    информация об организации по ID
    """
    data = await OrganizationService.get_by_id(org_id, session)
    if not data:
        raise HTTPException(status_code=404, detail="Organization not found")

    return OrganizationDetailSchema.model_validate(data)


@router.get("/buildings", response_model=list[BuildingSchema])
async def get_buildings(session: AsyncSession = Depends(get_session)):
    """
    список всех зданий
    """
    buildings = await BuildingService.get_all(session)
    return buildings
