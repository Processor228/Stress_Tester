from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#  stashed postgres password as OS variable
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{os.environ["POSTGRES_PSW"]}@localhost:5432/Stress'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
