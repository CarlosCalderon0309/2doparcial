import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, Base, User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal()

    yield db

    db.close()
    transaction.rollback()
    connection.close()

def test_create_user(client):
    response = client.post("/users/", json={
        "nombre": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "123 Test St",
        "telefono": "1234567890",
        "is_active": True,
        "fecha_creacion": "2024-09-27"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "testuser"

def test_read_user(client):

    create_response = client.post("/users/", json={
        "nombre": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "123 Test St",
        "telefono": "1234567890",
        "is_active": True,
        "fecha_creacion": "2024-09-27"
    })
    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "testuser"

def test_update_user(client):
    create_response = client.post("/users/", json={
        "nombre": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "123 Test St",
        "telefono": "1234567890",
        "is_active": True,
        "fecha_creacion": "2024-09-27"
    })
    user_id = create_response.json()["id"]

    response = client.put(f"/users/{user_id}", json={"nombre": "updateduser"})
    assert response.status_code == 200
    assert response.json()["nombre"] == "updateduser"

def test_delete_user(client):

    create_response = client.post("/users/", json={
        "nombre": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "fecha_nacimiento": "1990-01-01",
        "direccion": "123 Test St",
        "telefono": "1234567890",
        "is_active": True,
        "fecha_creacion": "2024-09-27"
    })
    user_id = create_response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully"}

def test_read_non_existent_user(client):
    response = client.get("/users/999/")
    assert response.status_code == 404
