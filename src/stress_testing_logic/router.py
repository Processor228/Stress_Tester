from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db_connection import get_db

from src.room_manage_logic import room_crud
from src.stress_testing_logic import testing_impl, schemas

router = APIRouter()


@router.post("/test/run_room/{room_id}", response_model=schemas.TestingOutput)
def run_room(room_id: int, db: Session = Depends(get_db)):
    room = room_crud.get_room(db, room_id)
    return testing_impl.test_code(room)
