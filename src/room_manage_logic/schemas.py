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

