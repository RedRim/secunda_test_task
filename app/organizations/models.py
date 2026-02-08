from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Activity(Base):
    """
    модель вида деятельности с древовидной структурой
    """
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("level <= 3", name="check_activity_level"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    level = Column(Integer, nullable=False, default=1)

    parent = relationship("Activity", remote_side="[Activity.id]")


class Building(Base):
    """
    модель здания с географическими координатами
    """
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class Organization(Base):
    """
    Модель организации
    """
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building")


class OrganizationPhone(Base):
    """
    Телефон организации
    """
    __tablename__ = "organization_phones"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    phone = Column(String, nullable=False)


class OrganizationActivity(Base):
    """
    связь организации и вида деятельности (many-to-many)
    """
    __tablename__ = "organization_activities"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
