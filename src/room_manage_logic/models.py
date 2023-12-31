from sqlalchemy import Boolean, ForeignKey, Integer, String, Column
from sqlalchemy.dialects import registry
from sqlalchemy.orm import relationship
from src.db_connection import Base
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    bruteforce_src = mapped_column(String, nullable=False)
    test_gen_src = mapped_column(String, nullable=False)
    tested_src = mapped_column(String, nullable=False)
    # lang = mapped_column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="rooms")
