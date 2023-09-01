from pydantic import BaseModel


class RoomBase(BaseModel):
    bruteforce_src: str
    test_gen_src: str
    tested_src: str
    # lang: str


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


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


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
