from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..Database import Base
from ..routers.todos import getDB, getCurrentUser
from ..Main import app
from fastapi.testclient import TestClient

# Although I have PostgreSQL as my production database, I can still use sqLite as my local testing database
# We will end up with 2 databases; one for production and one for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "joelduran", "id": 1, "userRole": "admin"}


app.dependency_overrides[getDB] = override_get_db
app.dependency_overrides[getCurrentUser] = override_get_current_user


client = TestClient(app)


def test_read_all_authenticated():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
