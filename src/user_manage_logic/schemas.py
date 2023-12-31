from pydantic import BaseModel

from src.room_manage_logic.schemas import Room


class UserBase(BaseModel):
    email: str
    username: str
    role: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: int
    rooms: list[Room] = []

    class Config:
        orm_mode = True

