from typing import Annotated

from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db_connection import get_db

from src.room_manage_logic import room_crud, schemas

from src.user_logic import schemas as user_schemas, user_crud
from src.user_logic.user_crud import get_current_user

router = APIRouter(prefix="/rooms")


@router.put("/update", response_model=schemas.Room)
def update_room(room: schemas.RoomBase,
                current_user: Annotated[user_schemas.User, Depends(get_current_user)],
                db: Session = Depends(get_db)):

    db_room = room_crud.get_room(db, room_id=current_user.room.id)

    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    return room_crud.updateCodeInRoom(db, room, db_room.id)


@router.get("/get", response_model=schemas.Room)
def get_room(current_user: Annotated[user_schemas.User, Depends(get_current_user)],
             db: Session = Depends(get_db)):
    db_room = room_crud.get_room(db, room_id=current_user.room.id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room
