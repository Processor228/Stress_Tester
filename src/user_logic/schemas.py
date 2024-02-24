from pydantic import BaseModel

from src.room_manage_logic.schemas import Room


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    room: Room

    class Config:
        orm_mode = True


class OperationInfo(BaseModel):
    info: str

