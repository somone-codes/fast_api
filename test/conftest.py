from src.fast_api import app
from src.schemas.settings import settings
from models import Base

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from alembic import command

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    yield TestClient(app)

@pytest.fixture()
def create_user(client: TestClient):
    user = {"email": "test_user@mail.com", "password": "testpass"}
    response = client.post("/users/", json=user)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user['password']
    return new_user