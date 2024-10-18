from sqlmodel import SQLModel, Field, Relationship, Column, String
from typing import Optional, List
from pydantic import EmailStr


class UserBase(SQLModel):
    email: EmailStr
    password: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(sa_column_kwargs={'unique': True})


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass


