from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
