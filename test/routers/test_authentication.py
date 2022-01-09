from src.schemas.token import Token
from schemas.settings import settings

from fastapi.testclient import TestClient
from jose import jwt


def test_login(client: TestClient, create_user):
    response = client.post("/login",
                           data={"username": create_user.get('email'), "password": create_user.get('password')})
    assert response.status_code == 200
    token = Token(**response.json())
    assert token.token_type == "bearer"
    payload = jwt.decode(token.access_token, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    assert payload.get("user_id") == create_user.get('id')
