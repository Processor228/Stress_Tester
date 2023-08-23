from fastapi.middleware.cors import CORSMiddleware
from db_conn import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import db_manipulations as crud
import subprocess
import os

"""
Just followed this guide and adjusted for my needs: https://fastapi.tiangolo.com/tutorial/sql-databases/
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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/rooms/create_one/{user_id}", response_model=schemas.Room)
def create_room(user_id: int, room: schemas.RoomCreate, db: Session = Depends(get_db)):
    return crud.create_user_room(db, room, user_id)


@app.put("/rooms/update/{room_id}", response_model=schemas.Room)
def update_room(room_id: int, room: schemas.Room, db: Session = Depends(get_db)):
    return crud.updateCodeInRoom(db, room)


@app.get("/rooms/get/{room_id}", response_model=schemas.Room)
def get_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


CONTAINERS_MAX: int = 5
CONTAINERS_NOW: int = 0


@app.get("/rooms/run/{room_id}")
def run_room(room_id: int, db: Session = Depends(get_db)):
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

    return stress_output

