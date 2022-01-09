from src.fast_api import app
from src.schemas.user import UserOut

from fastapi.testclient import TestClient

app_client = TestClient(app)


def test_create_users(client: TestClient):
    user = {"email": "test_user@mail.com", "password": "testpass"}
    response = client.post("/users/", json=user)
    assert response.status_code == 201
    new_user = UserOut(**response.json())
    assert new_user.email == user.get("email")
