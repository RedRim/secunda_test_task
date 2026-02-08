"""
скрипт заполнения базы данных тестовыми данными
"""
import asyncio

from sqlalchemy import select

from app.database import async_session_maker
from app.organizations.models import Activity, Building, Organization, OrganizationActivity, OrganizationPhone


async def seed_data():
    """
    создание тестовых данных в БД
    """
    async with async_session_maker() as session:
        # Создаем виды деятельности (дерево)
        food = Activity(name="Еда", parent_id=None, level=1)
        session.add(food)
        await session.flush()

        meat = Activity(name="Мясная продукция", parent_id=food.id, level=2)
        dairy = Activity(name="Молочная продукция", parent_id=food.id, level=2)
        session.add_all([meat, dairy])
        await session.flush()

        auto = Activity(name="Автомобили", parent_id=None, level=1)
        session.add(auto)
        await session.flush()

        truck = Activity(name="Грузовые", parent_id=auto.id, level=2)
        passenger = Activity(name="Легковые", parent_id=auto.id, level=2)
        session.add_all([truck, passenger])
        await session.flush()

        parts = Activity(name="Запчасти", parent_id=passenger.id, level=3)
        accessories = Activity(name="Аксессуары", parent_id=passenger.id, level=3)
        session.add_all([parts, accessories])
        await session.flush()

        # Создаем здания
        buildings_data = [
            Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55, longitude=37),
                Building(address="г. Новосибирск, ул. Блюхера, 32/1", latitude=55, longitude=82),
            Building(address="г. Москва, ул. Тверская 10", latitude=55, longitude=37),
        ]
        for building in buildings_data:
            session.add(building)
        await session.flush()

        # Получаем ID зданий
        result = await session.execute(select(Building))
        buildings = result.scalars().all()

        # Создаем организации
        org1 = Organization(name='ООО "Рога и Копыта"', building_id=buildings[1].id)
        org2 = Organization(name='ООО "Молочный завод"', building_id=buildings[0].id)
        org3 = Organization(name='ООО "АвтоТрейд"', building_id=buildings[2].id)
        org4 = Organization(name='ИП "Мясная лавка"', building_id=buildings[0].id)

        session.add_all([org1, org2, org3, org4])
        await session.flush()

        # Добавляем телефоны
        phones = [
            OrganizationPhone(organization_id=org1.id, phone="79932992939"),
            OrganizationPhone(organization_id=org1.id, phone="79991234567"),
            OrganizationPhone(organization_id=org1.id, phone="79991234567"),
            OrganizationPhone(organization_id=org2.id, phone="79991234567"),
            OrganizationPhone(organization_id=org3.id, phone="79991234567"),
            OrganizationPhone(organization_id=org4.id, phone="79991234567"),
        ]
        for phone in phones:
            session.add(phone)

        # Связываем организации с деятельностью
        activities = [
            OrganizationActivity(organization_id=org1.id, activity_id=meat.id),
            OrganizationActivity(organization_id=org1.id, activity_id=dairy.id),
            OrganizationActivity(organization_id=org2.id, activity_id=dairy.id),
            OrganizationActivity(organization_id=org3.id, activity_id=parts.id),
            OrganizationActivity(organization_id=org3.id, activity_id=accessories.id),
            OrganizationActivity(organization_id=org4.id, activity_id=meat.id),
        ]
        for activity in activities:
            session.add(activity)

        await session.commit()
        print("Тестовые данные успешно добавлены!")


if __name__ == "__main__":
    asyncio.run(seed_data())
