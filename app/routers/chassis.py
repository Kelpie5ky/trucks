from fastapi import APIRouter, Depends, HTTPException
from app.databases.database import get_session
from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import selectinload

from app.models.chassis import *

from app.utils.relationship_util import create_related_objects

router = APIRouter(
    prefix="/chassis",
    tags=["chassis"],
    responses={404: {"description": "Not found"}},
)


@router.post('/add', response_model=ChassisDetailed)
async def add_chassis(*, session: Session = Depends(get_session), chassis_with_properties: ChassisCreateWithProperties):
    new_chassis = Chassis(**chassis_with_properties.model_dump(exclude={"chassis_property_set"}))

    session.add(new_chassis)
    session.commit()
    session.refresh(new_chassis)

    chassis_property_sets = await create_related_objects(
        parent_instance=new_chassis,
        related_data_list=chassis_with_properties.chassis_property_set,
        related_class=ChassisPropertySet,
        parent_id_name="chassis_id"
    )
    session.add_all(chassis_property_sets)
    session.commit()

    return new_chassis

@router.get('/', response_model=List[Chassis])
async def get_chassis_list(*, session: Session = Depends(get_session)):
    chassis_list = session.exec(select(Chassis)).scalars().all()
    return chassis_list

@router.get('/{chassis_id}', response_model=ChassisDetailed)
def get_chassis_by_id(*, session: Session = Depends(get_session), chassis_id: int):
    chassis = session.exec(
        select(Chassis)
        .options(selectinload(Chassis.chassis_property_set))
        .where(Chassis.id == chassis_id)).first()
    if not chassis:
        raise HTTPException(status_code=404, detail="Chassis not found.")

    return chassis





@router.delete("/delete/{chassis_id}")
def delete_chassis_by_id(*, session: Session = Depends(get_session), chassis_id: int):
    chassis = session.get(Chassis, chassis_id)
    if not chassis:
        raise HTTPException(status_code=404, detail="Truck not found")
    session.delete(chassis)
    session.commit()
    return {"ok": True}