from sqlalchemy.orm import Session
from src.room_manage_logic import models, schemas
from enum import Enum


class Lang(Enum):
    PY = "py"
    CPP = "cpp"
    C = "C"


def create_room(db: Session, user_id: int) -> schemas.Room:
    db_item = models.Room(test_gen_src="", bruteforce_src="", tested_src="", checker_src="", user_id=user_id,
                          bruteforce_lang=Lang.PY.value, test_gen_lang=Lang.PY.value, tested_lang=Lang.PY.value,
                          checker_lang=Lang.PY.value)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def updateCodeInRoom(db: Session, room: schemas.RoomBase, room_id: int) -> schemas.Room:
    db.query(models.Room).filter(models.Room.id == room_id).update(dict(bruteforce_src=room.bruteforce_src,
                                                                        tested_src=room.tested_src,
                                                                        test_gen_src=room.test_gen_src,
                                                                        checker_src=room.checker_src,
                                                                        bruteforce_lang=room.bruteforce_lang,
                                                                        test_gen_lang=room.test_gen_lang,
                                                                        tested_lang=room.tested_lang,
                                                                        checker_lang=room.checker_lang
                                                                        ))
    res = db.query(models.Room).filter(models.Room.id == room_id).first()
    db.commit()
    db.refresh(res)
    return res


def get_room(db: Session, room_id: int) -> schemas.Room:
    print(room_id)
    res = db.query(models.Room).get(room_id)
    return res


def delete_room(db: Session, room_id: int) -> int:
    res = db.query(models.Room).filter(models.Room.id == room_id).delete()
    db.commit()
    return res

