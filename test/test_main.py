from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/todos/")
    assert response.status_code in (401, 403)  # Unauthorized without token

# Contoh test untuk auth
def test_login():
    response = client.post("/token", data={"username": "test", "password": "test"})
    assert response.status_code == 200
    assert "access_token" in response.json()