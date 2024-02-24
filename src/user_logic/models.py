from sqlalchemy import String, Column
from src.db_connection import Base
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from src.room_manage_logic.models import Room


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String)

    room = relationship("Room", back_populates="user", uselist=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        room = Room()
        room.user = self

