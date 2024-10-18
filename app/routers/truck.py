from fastapi import APIRouter, Depends, HTTPException
from app.databases.database import get_session
from sqlalchemy import select
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import selectinload

from app.models.truck import *
from app.models.chassis import Chassis, ChassisCreate


router = APIRouter(
    prefix="/trucks",
    tags=["trucks"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', response_model=List[Truck])
async def get_trucks(*, session: Session = Depends(get_session)):
    trucks = session.exec(select(Truck)).scalars().all()

    return trucks

@router.get("/{truck_id}", response_model=Truck)
def get_truck_by_id(*, session: Session = Depends(get_session), truck_id: int):

    truck = session.exec(
        select(Truck)
        .options(selectinload(Truck.chassis))
        .where(Truck.id == truck_id)
    ).first()
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found.")

    return truck

@router.post('/add')
async def add_truck(*, session: Session = Depends(get_session), truck: TruckCreate):
    if truck.chassis_id:
        chassis = session.get(Chassis, truck.chassis_id)
        if not chassis:
            raise HTTPException(status_code=404, detail="Chassis not found.")
        chassis_id = truck.chassis_id
    elif truck.chassis:
        new_chassis = Chassis.from_orm(truck.chassis)
        session.add(new_chassis)
        session.commit()
        session.refresh(new_chassis)
        chassis_id = new_chassis.id
    else:
        raise HTTPException(status_code=400, detail="Either chassis_id or chassis data must be provided.")

    add_truck = Truck(
        title=truck.title,
        truck_type=truck.truck_type,
        chassis_id=chassis_id
    )
    session.add(add_truck)
    session.commit()
    session.refresh(add_truck)
    return add_truck

#Edit truck by id
# @router.patch('/edit/{truck_id}')