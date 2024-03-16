from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#  stashed postgres password as OS variable ('dialect+driver://username:password@host:port/database')
SQLALCHEMY_DATABASE_URL = f'postgresql://{os.environ["POSTGRES_USR"]}:{os.environ["POSTGRES_PSW"]}' \
                          f'@{os.environ["POSTGRES_HOST"]}:{os.environ["POSTGRES_PORT"]}/{os.environ["POSTGRES_DB_NAME"]}'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
