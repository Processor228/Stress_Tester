from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update
from bcrypt import hashpw
from passlib.context import CryptContext


import models
import schemas


def get_password_hash(password):
    return pwd_context.hash(password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int) -> schemas.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_name(db: Session, username: str) -> schemas.User:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> schemas.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


#   TODO normal hashing
def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    fake_hashed_password = user.password
    db_user = models.User(email=user.email, hashed_password=get_password_hash(fake_hashed_password),
                          username=user.username, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
