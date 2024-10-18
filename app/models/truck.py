from sqlmodel import SQLModel, Field, Relationship, Column, String
from typing import Optional, List, TYPE_CHECKING

from app.models.chassis import ChassisCreate


class TruckBase(SQLModel):
    title: str
    truck_type: str

    chassis_id: int = Field(default=None, foreign_key="chassis.id")
    # image_set_id: int
    # super_structure_list_id: int
    # user_id: int


class Truck(TruckBase, table=True):
    id: int = Field(default=None, primary_key=True)
    margin: int = Field(default=750000)

    chassis: "Chassis" = Relationship(back_populates="trucks")

class TruckCreate(TruckBase):
    chassis_id: Optional[int] = None
    chassis: Optional["ChassisCreate"] = None


class TruckUpdate(TruckBase):
    pass