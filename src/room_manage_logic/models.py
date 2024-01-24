from sqlalchemy import String, Column
from src.db_connection import Base
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    bruteforce_src = mapped_column(String, nullable=False)
    test_gen_src = mapped_column(String, nullable=False)
    tested_src = mapped_column(String, nullable=False)
    checker_src = mapped_column(String, nullable=False)
    bruteforce_lang = mapped_column(String, nullable=False)
    test_gen_lang = mapped_column(String, nullable=False)
    tested_lang = mapped_column(String, nullable=False)
    checker_lang = mapped_column(String, nullable=False)
