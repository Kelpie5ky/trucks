from fastapi import APIRouter, Depends, HTTPException
from app.databases.database import get_session
from sqlalchemy import select
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError

from app.models.chassis import *


router = APIRouter(
    prefix="/chassis",
    tags=["chassis"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[Chassis])
async def get_chassis_list(*, session: Session = Depends(get_session)):
    chassis_list = session.exec(select(Chassis)).scalars().all()
    return chassis_list

@router.get("/{chassis_id}", response_model=Chassis)
def get_chassis_by_id(*, session: Session = Depends(get_session), chassis_id: int):
    chassis = session.get(Chassis, chassis_id)

    if not chassis:
        raise HTTPException(status_code=404, detail="Film not found.")

    return chassis

@router.post('/add')
async def add_chassis(*, session: Session = Depends(get_session), chassis: ChassisCreate):
    add_chassis = Chassis.from_orm(chassis)
    session.add(add_chassis)
    session.commit()
    session.refresh(add_chassis)
    return chassis

