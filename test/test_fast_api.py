try:
    from src.fast_api import app
except ImportError:
    # doing this because if src is not added as python path we get this issue
    from pathlib import Path
    from os.path import join
    from sys import path as sys_path

    sys_path.append(join(Path(__file__).parents[1], "src"))
    from src.fast_api import app

from fastapi.testclient import TestClient


app_client = TestClient(app)


def test_index():
    response = app_client.get("/")
    assert response.status_code == 200
    assert response.text.strip("\"") == "Welcome to FastAPI DEMO APP!!!"
