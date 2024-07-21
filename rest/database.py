from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from config import (
    POSTGRES_USER, 
    POSTGRES_PASSWORD, 
    POSTGRES_HOST, 
    POSTGRES_PORT, 
    POSTGRES_DB
)


DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)

def get_session() -> Generator[Session, None, None]:
    with session_maker() as session:
        yield session