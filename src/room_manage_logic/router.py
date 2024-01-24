from fastapi import APIRouter, Request, Response, Depends, HTTPException
from sqlalchemy.orm import Session

from src.db_connection import get_db

from src.room_manage_logic import room_crud, schemas

router = APIRouter(prefix="/rooms")


@router.post("/create_one", response_model=schemas.Room)
def create_room(db: Session = Depends(get_db)):
    return room_crud.create_room(db)


@router.put("/update/{room_id}", response_model=schemas.Room)
def update_room(room_id: int, room: schemas.RoomBase, db: Session = Depends(get_db)):
    db_room = room_crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    return room_crud.updateCodeInRoom(db, room, room_id)


@router.get("/get/{room_id}", response_model=schemas.Room)
def get_room(room_id: int, db: Session = Depends(get_db)):
    db_room = room_crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


@router.delete("/delete/{room_id}", response_model=int)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    deleted = room_crud.delete_room(db, room_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Room to delete is not found")
    return deleted
