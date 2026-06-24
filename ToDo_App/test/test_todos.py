from fastapi import status
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.status import HTTP_201_CREATED
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


#     When you pass test_todo as an argument to a test function, pytest sees that parameter name, finds the
#     matching fixture, runs it, and injects whatever it returns into your test.


def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "complete": False,
        "title": "Learn to code",
        "description": "Need to learn everyday",
        "id": 1,
        "priority": 5,
        "owner": 1,
    }


def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "New todo",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }

    response = client.post("/todo/", json=request_data)
    assert response.status_code == HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        "title": "Change title of the todo",
        "description": "Need to learn everyday",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Change title of the todo"


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Change title of the todo",
        "description": "Need to learn everyday",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
