"""
сервисы для работы с организациями и зданиями
"""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.organizations.models import Activity, Building, Organization, OrganizationActivity, OrganizationPhone


class OrganizationService:
    """
    сервис для работы с организациями
    """

    @staticmethod
    async def get_by_building(building_id: int, session: AsyncSession):
        """
        получить организации по ID здания с информацией о здании
        """
        stmt = (
            select(Organization)
            .where(Organization.building_id == building_id)
            .options(joinedload(Organization.building))
        )
        result = await session.execute(stmt)
        return result.unique().scalars().all()

    @staticmethod
    async def get_by_activity(activity_id: int, session: AsyncSession):
        """
        получить организации по виду деятельности
        Включает все дочерние виды деятельности
        """
        activity_ids = await OrganizationService._get_activity_subtree(activity_id, session)

        stmt = (
            select(Organization)
            .join(OrganizationActivity)
            .where(OrganizationActivity.activity_id.in_(activity_ids))
            .distinct()
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_by_radius(lat: float, lon: float, radius: float, session: AsyncSession):
        """
        получить организации в радиусе от точки
        """
        stmt = select(Organization).join(Building).where(
            func.sqrt(
                func.pow(Building.latitude - lat, 2) + func.pow(Building.longitude - lon, 2)
            ) * 111000 <= radius
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_by_rectangle(
        lat_min: float, lat_max: float, lon_min: float, lon_max: float, session: AsyncSession
    ):
        """
        Получить организации в прямоугольной области
        """
        stmt = (
            select(Organization)
            .join(Building)
            .where(
                Building.latitude >= lat_min,
                Building.latitude <= lat_max,
                Building.longitude >= lon_min,
                Building.longitude <= lon_max,
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(org_id: int, session: AsyncSession):
        """
        получить детальную информацию об организации
        """
        stmt = select(Organization).where(Organization.id == org_id)
        result = await session.execute(stmt)
        org = result.scalar_one_or_none()

        if not org:
            return None

        # Получаем телефоны
        phone_stmt = select(OrganizationPhone).where(OrganizationPhone.organization_id == org_id)
        phone_result = await session.execute(phone_stmt)
        phones = phone_result.scalars().all()

        # Получаем активности
        activity_stmt = (
            select(Activity)
            .join(OrganizationActivity)
            .where(OrganizationActivity.organization_id == org_id)
        )
        activity_result = await session.execute(activity_stmt)
        activities = activity_result.scalars().all()

        # Получаем здание
        building_stmt = select(Building).where(Building.id == org.building_id)
        building_result = await session.execute(building_stmt)
        building = building_result.scalar_one_or_none()

        return {
            "id": org.id,
            "name": org.name,
            "phones": [p.phone for p in phones],
            "activities": activities,
            "building": building,
        }

    @staticmethod
    async def search_by_name(name: str, session: AsyncSession):
        """
        поиск организаций по названию
        """
        stmt = select(Organization).where(Organization.name.ilike(f"%{name}%"))
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def _get_activity_subtree(activity_id: int, session: AsyncSession) -> list[int]:
        """
        рекурсивное получение всех ID активностей в поддереве
        """
        result_ids = [activity_id]

        stmt = select(Activity).where(Activity.parent_id == activity_id)
        result = await session.execute(stmt)
        children = result.scalars().all()

        for child in children:
            child_ids = await OrganizationService._get_activity_subtree(child.id, session)
            result_ids.extend(child_ids)

        return result_ids


class BuildingService:
    """
    Сервис для работы со зданиями
    """

    @staticmethod
    async def get_all(session: AsyncSession):
        """
        получить список всех зданий
        """
        stmt = select(Building)
        result = await session.execute(stmt)
        return result.scalars().all()
