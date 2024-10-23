from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

from .image_set import *
from .chassis import Chassis, ChassisDetailed, ChassisCreateWithProperties


class TruckBase(SQLModel):
    title: str
    truck_type: str

    chassis_id: int = Field(default=None, foreign_key="chassis.id")



class Truck(TruckBase, table=True):
    id: int = Field(default=None, primary_key=True)
    margin: int = Field(default=750000)

    chassis: Optional["Chassis"] = Relationship(back_populates="trucks")
    image_set: List["ImageSet"] = Relationship(back_populates="truck")


class TruckCreate(TruckBase):
    chassis_id: Optional[int] = None
    chassis: Optional["ChassisCreateWithProperties"] = None



class TruckUpdate(SQLModel):
    title: Optional[str] = None
    truck_type: Optional[str] = None
    chassis_id: Optional[int] = None
    chassis: Optional[ChassisCreateWithProperties] = None
    margin: Optional[int] = None
    image_ids: Optional[List[int]] = None


class TruckDetailed(TruckBase):
    id: int
    margin: int
    chassis: "ChassisDetailed"
    image_set: Optional[List["ImageSet"]]

