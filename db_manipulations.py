from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update
from bcrypt import hashpw

import models
import schemas


def get_user(db: Session, user_id: int) -> schemas.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


#   TODO normal hashing
def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    fake_hashed_password = hashpw(str.encode(user.password), str.encode("notreally"))
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, name=user.name, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_room(db: Session, room: schemas.RoomCreate, user_id: int) -> schemas.Room:
    db_item = models.Room(**room.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def updateCodeInRoom(db: Session, room: schemas.Room) -> schemas.Room:
    db.query(models.Room).filter(models.Room.id == room.id).update(dict(bruteforce_src=room.bruteforce_src,
                                                                        tested_src=room.tested_src,
                                                                        test_gen_src=room.test_gen_src))
    res = db.query(models.Room).filter(models.Room.id == room.id).first()
    return res


def get_room(db: Session, room_id: int) -> schemas.Room:
    return db.query(models.Room).filter(models.Room.id == room_id).first()
