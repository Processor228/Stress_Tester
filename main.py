import datetime
from datetime import timedelta, datetime

from starlette.middleware.cors import CORSMiddleware
from db_conn import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from schemas import TokenData, Token

from sqlalchemy.orm import Session
import db_manipulations as crud
import subprocess
import os

"""
Just followed this guide and adjusted for my needs: https://fastapi.tiangolo.com/tutorial/sql-databases/
and also this:                                      https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""

import models
import schemas

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_name(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_name(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=Token)
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


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)]
):
    return current_user


@app.post("/users/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# @app.get("/users/get_rooms", response_model=schemas.)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.post("/rooms/create_one/", response_model=schemas.Room)
def create_room(current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                db: Session = Depends(get_db)):
    return crud.create_user_room(db, current_user.id)


@app.put("/rooms/update/{room_id}", response_model=schemas.Room)
def update_room(room_id: int, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
                room: schemas.RoomBase, db: Session = Depends(get_db)):
    return crud.updateCodeInRoom(db, room, room_id)


@app.get("/rooms/get/{room_id}", response_model=schemas.Room)
def get_room(room_id: int, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
             db: Session = Depends(get_db)):
    db_room = crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


CONTAINERS_MAX: int = 5
CONTAINERS_NOW: int = 0


@app.get("/rooms/run/{room_id}")
def run_room(room_id: int, current_user: Annotated[schemas.User, Depends(get_current_active_user)],
             db: Session = Depends(get_db)):
    global CONTAINERS_MAX, CONTAINERS_NOW
    db_room = crud.get_room(db, room_id)
    stress_output: str
    if CONTAINERS_NOW >= CONTAINERS_MAX:
        stress_output = "wait 'till server can handle your request"
    else:
        # this is c++ testing implementation
        CONTAINERS_NOW += 1
        subprocess.run(["mkdir", "test_dir/stress{}".format(CONTAINERS_NOW)])

        with open("test_dir/stress{}/bruteforce_src.cpp".format(CONTAINERS_NOW), "w") as wr:
            wr.write(db_room.bruteforce_src)
        with open("test_dir/stress{}/test_gen_src.cpp".format(CONTAINERS_NOW), "w") as wr:
            wr.write(db_room.test_gen_src)
        with open("test_dir/stress{}/tested_src.cpp".format(CONTAINERS_NOW), "w") as wr:
            wr.write(db_room.tested_src)

        subprocess.run("cat test_script.sh > test_dir/stress{}/test.sh".format(CONTAINERS_NOW), shell=True)
        subprocess.run("cat test_Dockerfile > test_dir/stress{}/Dockerfile".format(CONTAINERS_NOW), shell=True)

        # --------------( building the image )------------------ #
        subprocess.run(
            ["docker", "build", "-t", "stress_{}".format(CONTAINERS_NOW), "test_dir/stress{}".format(CONTAINERS_NOW)])

        # ------------ ( starting the container) --------------- #
        container_id = str(subprocess.check_output(
            ["docker", "run", "-t", "-d", "stress_{}:latest".format(CONTAINERS_NOW)]))[2:-3]
        print(container_id)

        # ------------ ( invoking testing procedure ) ---------- #
        stress_output = subprocess.check_output(["docker", "exec", container_id, "bash", "test.sh"]).decode("utf-8")
        subprocess.run(["docker", "kill", container_id])
    print(stress_output)
    return dict(verdict=stress_output)

