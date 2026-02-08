from pydantic import BaseModel


class ActivityBase(BaseModel):
    """
    Базовая схема вида деятельности
    """
    name: str
    parent_id: int | None = None


class ActivitySchema(ActivityBase):
    """
    полная схема вида деятельности
    """
    id: int
    level: int

    class Config:
        from_attributes = True


class BuildingBase(BaseModel):
    """
    базовая схема здания
    """
    address: str
    latitude: float
    longitude: float


class BuildingSchema(BuildingBase):
    """
    Полная схема здания
    """
    id: int

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    """
    Базовая схема организации
    """
    name: str
    building_id: int


class OrganizationSchema(OrganizationBase):
    """
    схема организации для списков
    """
    id: int

    class Config:
        from_attributes = True


class OrganizationWithBuildingSchema(OrganizationBase):
    """
    Схема организации с информацией о здании
    """
    id: int
    building: BuildingSchema

    class Config:
        from_attributes = True


class OrganizationDetailSchema(BaseModel):
    """
    детальная схема организации со всеми связями
    """
    id: int
    name: str
    phones: list[str]
    building: BuildingSchema
    activities: list[ActivitySchema]

    class Config:
        from_attributes = True
