from fastapi import APIRouter, Depends, HTTPException
from app.databases.database import get_session
from app.models.user import *
from sqlalchemy import select
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[User])
async def get_users(*, session: Session = Depends(get_session)):
    users = session.exec(select(User)).scalars().all()
    return users

@router.post('/create')
async def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    try:
        add_user = User.from_orm(user)
        session.add(add_user)
        session.commit()
        session.refresh(add_user)
        return user
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")