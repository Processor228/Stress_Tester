import datetime
from datetime import timedelta, datetime

from starlette.middleware.cors import CORSMiddleware

import src.user_manage_logic.models
from src.db_connection import SessionLocal, engine, Base
from fastapi import Depends, FastAPI, HTTPException, status

from .user_manage_logic.router import router as user_management_endpoints
from .room_manage_logic.router import router as room_management_endpoints
from .oauth.router import router as oauth_management_endpoints


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

app.include_router(user_management_endpoints)
app.include_router(room_management_endpoints)
app.include_router(oauth_management_endpoints)
