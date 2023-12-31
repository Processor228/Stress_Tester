from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.db_connection import get_db

from src.room_manage_logic import room_crud, schemas
from src.user_manage_logic.user_crud import get_user_by_name, authenticate_user, get_current_active_user

import src.user_manage_logic.schemas as user_schemas


router = APIRouter()


@router.post("/rooms/create_one/", response_model=schemas.Room)
def create_room(current_user: Annotated[user_schemas.User, Depends(get_current_active_user)],
                db: Session = Depends(get_db)):
    return room_crud.create_user_room(db, current_user.id)


@router.put("/rooms/update/{room_id}", response_model=schemas.Room)
def update_room(room_id: int, current_user: Annotated[user_schemas.User, Depends(get_current_active_user)],
                room: schemas.RoomBase, db: Session = Depends(get_db)):
    return room_crud.updateCodeInRoom(db, room, room_id)


@router.get("/rooms/get/{room_id}", response_model=schemas.Room)
def get_room(room_id: int, current_user: Annotated[user_schemas.User, Depends(get_current_active_user)],
             db: Session = Depends(get_db)):
    db_room = room_crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


# TODO delete endpoint
