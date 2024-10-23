from sqlmodel import SQLModel, Field, Relationship, Column, String
from typing import Optional, List, TYPE_CHECKING


from .truck import *
from .chassis_property_set import *

class ChassisBase(SQLModel):
    brand: str
    model: str
    wheel_base: str
    price: int

class Chassis(ChassisBase, table=True):
    id: int = Field(default=None, primary_key=True)
    trucks: List["Truck"] = Relationship(back_populates="chassis")
    chassis_property_set: List["ChassisPropertySet"] = Relationship(back_populates="chassis", cascade_delete=True)


class ChassisCreateWithProperties(ChassisBase):
    chassis_property_set: Optional[List["ChassisPropertySetCreate"]]


class ChassisDetailed(ChassisBase):
    id: int
    chassis_property_set: List["ChassisPropertySet"]

class ChassisUpdate(SQLModel):
    pass
