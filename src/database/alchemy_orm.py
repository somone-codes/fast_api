from schemas.settings import settings
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

_SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(_SQLALCHEMY_DATABASE_URL)

_SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


def get_db():
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
