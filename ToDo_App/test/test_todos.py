from fastapi import status
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..Database import Base
from ..routers.todos import getDB, getCurrentUser
from ..Main import app
from fastapi.testclient import TestClient
import pytest
from ..Models import Todos

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


@pytest.fixture()
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner=1,
    )

    # Make sure that for the db you are using TestingSessionLocal
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "complete": False,
            "title": "Learn to code",
            "description": "Need to learn everyday",
            "id": 1,
            "priority": 5,
            "owner": 1,
        }
    ]
