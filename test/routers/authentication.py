from src.schemas.token import Token
from ..database import client, session  # This is required as we are using client fixture which uses session
from schemas.settings import settings

from fastapi.testclient import TestClient
import pytest
from jose import jwt


@pytest.fixture()
def create_user(client: TestClient):
    user = {"email": "test_user@mail.com", "password": "testpass"}
    response = client.post("/users/", json=user)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user['password']
    return new_user



def test_login(client: TestClient, create_user):
    response = client.post("/login",
                           data={"username": create_user.get('email'), "password": create_user.get('password')})
    assert response.status_code == 200
    token = Token(**response.json())
    assert token.token_type == "bearer"
    payload = jwt.decode(token.access_token, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    assert payload.get("user_id") == create_user.get('id')