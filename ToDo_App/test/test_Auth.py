from .utils import *
from ..routers.Auth import (
    createAccessToken,
    getDB,
    authenticateUser,
    SECRET_KEY,
    ALGORITHM,
)
from jose import jwt
from datetime import timedelta

app.dependency_overrides[getDB] = override_get_db


def test_authenticate_user(test_User):
    db = TestingSessionLocal()
    authenticated_user = authenticateUser(test_User.username, "testpassword", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_User.username

    non_existent_user = authenticateUser("WrongUserName", "testpassword", db)
    assert non_existent_user is False

    wrong_password_user = authenticateUser(test_User.username, "wrongpassword", db)
    assert wrong_password_user is False


def test_create_access_token():
    username = "testuser"
    userID = 1
    role = "user"
    expiresDelta = timedelta(days=1)

    token = createAccessToken(username, userID, role, expiresDelta)

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == userID
    assert decoded_token["role"] == role
