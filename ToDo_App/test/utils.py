from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..Database import Base
from ..Main import app
from fastapi.testclient import TestClient
import pytest
from ..Models import Todos, Users
from ..routers.Auth import bcrypt_context


# Although I have PostgreSQL as my production database, I can still use sqLite as my local testing database
# We will end up with 2 databases; one for production and one for testing, This is in the utils.py file because
# it is reusable code and we moved it here to reuse it in other places
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


@pytest.fixture
def test_User():
    user = Users(
        username="joelduran",
        email="joelduran@email.com",
        firstName="joel",
        lastName="duran",
        hashedPWD=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM Users;"))
        connection.commit()
