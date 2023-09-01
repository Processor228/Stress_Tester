from sqlalchemy import Boolean, ForeignKey, Integer, String, Column
from sqlalchemy.dialects import registry
from sqlalchemy.orm import relationship
from db_conn import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = mapped_column(String, nullable=False)
    role = mapped_column(Integer, nullable=False)
    email = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String)

    rooms = relationship("Room", back_populates="user")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    bruteforce_src = mapped_column(String, nullable=False)
    test_gen_src = mapped_column(String, nullable=False)
    tested_src = mapped_column(String, nullable=False)
    # lang = mapped_column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="rooms")
