from pydantic import BaseModel


class RoomBase(BaseModel):
    bruteforce_src: str
    test_gen_src: str
    tested_src: str
    # lang: str


class RoomCreate(RoomBase):
    pass


"""{
    "bruteforce_src": "print('hello')",
    "test_gen_src": "print('test')",
    "tested_gen_src": "print('contest me !')"
}"""


class Room(RoomBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str
    role: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: int
    Rooms: list[Room] = []

    class Config:
        orm_mode = True
