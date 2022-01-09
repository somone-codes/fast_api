from src.schemas.token import Token
from schemas.settings import settings

from fastapi.testclient import TestClient
from jose import jwt
import pytest


def test_login(client: TestClient, create_user):
    response = client.post("/login",
                           data={"username": create_user.get('email'), "password": create_user.get('password')})
    assert response.status_code == 200
    token = Token(**response.json())
    assert token.token_type == "bearer"
    payload = jwt.decode(token.access_token, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    assert payload.get("user_id") == create_user.get('id')


@pytest.mark.parametrize("email, password, status_code", [
    ("invalid_user@email.com", "pass", 403,),
    ("invalid_user_2@email.com", "pass", 403,),
    ("invalid_user", "pass", 403,),
    (None, "pass", 422,),
    ("invalid_user", None, 422,)
])
def test_invalid_login(client: TestClient, email: str, password: str, status_code: int):
    response = client.post("/login",
                           data={"username": email, "password": password})
    assert response.status_code == status_code
