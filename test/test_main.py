from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app import crud, models, schemas

client = TestClient(app)

# Fixture untuk setup database
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = next(TestClient(app).app.dependency_overrides.get("get_db", lambda: None))
    # Buat user test
    user_data = schemas.UserCreate(username="test", password="test")
    crud.create_user(db, user_data)
    db.close()

def teardown_db():
    Base.metadata.drop_all(bind=engine)

def test_read_todos_unauthorized():
    response = client.get("/todos/")
    assert response.status_code == 401  # Unauthorized without token

def test_login_success():
    setup_db()
    try:
        login_data = {
            "username": "test",
            "password": "test"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()
    finally:
        teardown_db()