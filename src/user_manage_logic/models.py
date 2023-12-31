from sqlalchemy import Boolean, ForeignKey, Integer, String, Column
from src.db_connection import Base
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = mapped_column(String, nullable=False)
    role = mapped_column(Integer, nullable=False)
    email = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String)

    rooms = relationship("Room", back_populates="user")
