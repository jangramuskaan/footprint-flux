from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "sqlite:///footprint.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)