from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db_conn import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, nullable=False)
    role = mapped_column(Integer, nullable=False)
    email = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String)

    rooms = relationship("Room", back_populates="owner")


class Room(Base):
    __tablename__ = "rooms"

    id = mapped_column(Integer, primary_key=True, index=True)
    bruteforce_src = mapped_column(String, nullable=False)
    test_gen_src = mapped_column(String, nullable=False)
    tested_src = mapped_column(String, nullable=False)
    # lang = mapped_column(String, nullable=False)
    owner_id = mapped_column(Integer, ForeignKey("users.id"))

    owner = relationship(User, back_populates="rooms")
