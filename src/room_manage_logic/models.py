from sqlalchemy import String, Column, ForeignKey
from src.db_connection import Base
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, relationship


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="room")

    bruteforce_src = mapped_column(String, nullable=False, default="")
    test_gen_src = mapped_column(String, nullable=False, default="")
    tested_src = mapped_column(String, nullable=False, default="")
    checker_src = mapped_column(String, nullable=False, default="")
    bruteforce_lang = mapped_column(String, nullable=False, default="py")
    test_gen_lang = mapped_column(String, nullable=False, default="py")
    tested_lang = mapped_column(String, nullable=False, default="py")
    checker_lang = mapped_column(String, nullable=False, default="py")

    def __init__(self, **kwargs):
        super(Room, self).__init__(**kwargs)

