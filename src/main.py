from starlette.middleware.cors import CORSMiddleware

from src.db_connection import engine, Base
from fastapi import FastAPI

from .room_manage_logic.router import router as room_management_endpoints
from .stress_testing_logic.router import router as stress_testing_endpoints
from .user_logic.router import router as user_router

from .stress_testing_logic.testing_impl import prepare_containers

app = FastAPI(lifespan=prepare_containers)

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

app.include_router(room_management_endpoints)
app.include_router(stress_testing_endpoints)
app.include_router(user_router)
