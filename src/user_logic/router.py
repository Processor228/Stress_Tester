from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from src.db_connection import get_db

from src.oauth.OAuth import oauth2_scheme, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.user_logic import schemas as user_schemas, user_crud
from src.oauth import schemas as auth_schemas

from src.user_logic.user_crud import get_user_by_name, authenticate_user, get_current_active_user

import src.room_manage_logic.room_crud as room_crud

router = APIRouter()


@router.post("/token", response_model=auth_schemas.Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=user_schemas.User)
async def read_users_me(
        current_user: Annotated[user_schemas.User, Depends(get_current_active_user)]) -> user_schemas.User:
    # print(current_user.model_dump(mode='json'))
    print(current_user.username, current_user.id, current_user.room, current_user.email)
    return current_user


@router.post("/users/create", response_model=user_schemas.OperationInfo)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = user_crud.create_user(db=db, user=user)
    # created_room = room_crud.create_room(db, created_user.id)


    return user_schemas.OperationInfo(info="Success")
