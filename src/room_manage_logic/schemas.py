from pydantic import BaseModel


class Code(BaseModel):
    code_src: str
    lang: str


class RoomBase(BaseModel):
    bruteforce_src: Code
    test_gen_src: Code
    tested_src: Code
    checker_src: Code


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

