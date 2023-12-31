from sqlalchemy.orm import Session

from src.room_manage_logic import models, schemas


def create_user_room(db: Session, user_id: int) -> schemas.Room:
    db_item = models.Room(test_gen_src="", bruteforce_src="", tested_src="", user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def updateCodeInRoom(db: Session, room: schemas.RoomBase, room_id: int) -> schemas.Room:
    db.query(models.Room).filter(models.Room.id == room_id).update(dict(bruteforce_src=room.bruteforce_src,
                                                                        tested_src=room.tested_src,
                                                                        test_gen_src=room.test_gen_src))
    res = db.query(models.Room).filter(models.Room.id == room_id).first()
    db.commit()
    db.refresh(res)
    return res


def get_room(db: Session, room_id: int) -> schemas.Room:
    return db.query(models.Room).filter(models.Room.id == room_id).first()