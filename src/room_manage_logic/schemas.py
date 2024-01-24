from pydantic import BaseModel


class Code(BaseModel):
    code_src: str
    lang: str


class RoomUpdate(BaseModel):
    bruteforce: Code
    test_gen: Code
    tested: Code
    checker: Code


class RoomBase(BaseModel):
    bruteforce_src: str
    test_gen_src: str
    tested_src: str
    checker_src: str
    bruteforce_lang: str
    test_gen_lang: str
    tested_lang: str
    checker_lang: str


class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True

