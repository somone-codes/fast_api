from src.fast_api import app

from fastapi.testclient import TestClient


app_client = TestClient(app)


def test_index():
    response = app_client.get("/")
    assert response.status_code == 200
    assert response.text.strip("\"") == "Welcome to FastAPI DEMO APP!!!"
