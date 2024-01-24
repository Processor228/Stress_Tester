import datetime
from datetime import timedelta, datetime

from starlette.middleware.cors import CORSMiddleware

from src.db_connection import SessionLocal, engine, Base
from fastapi import Depends, FastAPI, HTTPException, status

from .room_manage_logic.router import router as room_management_endpoints
from .stress_testing_logic.router import router as stress_testing_endpoints


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

Base.metadata.create_all(bind=engine)

CONTAINERS_MAX: int = 5
CONTAINERS_NOW: int = 0

app.include_router(room_management_endpoints)
app.include_router(stress_testing_endpoints)
