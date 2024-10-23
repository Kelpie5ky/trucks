from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from app.databases.database import get_session
from sqlmodel import select, Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import selectinload

from app.models.truck import *
from app.models.chassis import Chassis, ChassisCreateWithProperties, ChassisDetailed
from app.models.chassis_property_set import ChassisPropertySet, ChassisPropertySetCreate

from app.utils.relationship_util import create_related_objects
from app.utils.upload_util import save_images

from app.services.truck_add_service import get_or_create_chassis, create_truck
from app.services.image_upload_service import upload_truck_images
from app.services.truck_update_service import update_truck


router = APIRouter(
    prefix="/trucks",
    tags=["trucks"],
    responses={404: {"description": "Not found"}},
)


@router.post('/add', response_model=TruckDetailed)
async def add_truck(
        truck_data: TruckCreate,
        image_ids: List[int] = None,
        session: Session = Depends(get_session)
):
    chassis_id = await get_or_create_chassis(session, truck_data)
    new_truck = await create_truck(session, truck_data, chassis_id, image_ids)
    return new_truck

@router.get('/', response_model=List[TruckDetailed])
async def get_trucks(*, session: Session = Depends(get_session)):
    trucks = session.exec(
        select(Truck)
        .options(
            selectinload(Truck.chassis).selectinload(Chassis.chassis_property_set)
        )
    ).all()
    return trucks

@router.get("/{truck_id}", response_model=TruckDetailed)
def get_truck_by_id(*, session: Session = Depends(get_session), truck_id: int):
    truck = session.exec(
        select(Truck)
        .options(selectinload(Truck.chassis).selectinload(Chassis.chassis_property_set))
        .where(Truck.id == truck_id)
).first()
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found.")

    return TruckDetailed.from_orm(truck)

@router.patch("/update/{truck_id}", response_model=TruckDetailed)
async def update_truck_by_id(
    truck_id: int,
    truck_data: TruckUpdate,
    session: Session = Depends(get_session)
):
    updated_truck = await update_truck(session, truck_id=truck_id, truck_data=truck_data)
    return updated_truck

@router.delete("/delete/{truck_id}")
async def delete_truck_by_id(*, session: Session = Depends(get_session), truck_id: int):
    truck = session.get(Truck, truck_id)
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    session.delete(truck)
    session.commit()
    return {"ok": True}

@router.delete("/delete/batch/")
async def batch_delete_trucks(*, session: Session = Depends(get_session), truck_ids: List[int]):
    trucks = session.exec(select(Truck).where(Truck.id.in_(truck_ids))).all()
    if not trucks:
        raise HTTPException(status_code=404, detail="Trucks not found")
    for truck in trucks:
        session.delete(truck)
    session.commit()
    return {"ok": True}