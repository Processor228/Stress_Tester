from typing import Annotated

from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.db_connection import get_db
from src.oauth import schemas

router = APIRouter()

