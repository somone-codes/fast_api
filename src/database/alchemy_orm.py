from os import getenv

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

_SQLALCHEMY_DATABASE_URL = getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./sql_app.db")

engine = create_engine(_SQLALCHEMY_DATABASE_URL)

_SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_db():
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
