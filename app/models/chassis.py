from sqlmodel import SQLModel, Field, Relationship, Column, String
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .truck import *


class ChassisBase(SQLModel):
    brand: str
    model: str
    wheel_base: str
    price: int

    # chassis_property_set_id: int


class Chassis(ChassisBase, table=True):
    id: int = Field(default=None, primary_key=True)
    trucks: "Truck" = Relationship(back_populates="chassis")

class ChassisCreate(ChassisBase):
    pass


class ChassisUpdate(ChassisBase):
    pass
