from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db_connection import get_db

from src.room_manage_logic import room_crud
from src.stress_testing_logic import testing_impl, schemas

import src.user_logic.schemas as user_schemas
from src.user_logic.user_crud import get_current_user

router = APIRouter()


@router.post("/test/run_room", response_model=schemas.TestingOutput)
def run_room(current_user: Annotated[user_schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    room = room_crud.get_room(db, current_user.room.id)
    return testing_impl.test_code(room)
