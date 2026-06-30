from starlette.status import HTTP_200_OK
from .utils import *
from ..routers.Users import getDB, getCurrentUser
from fastapi import status

app.dependency_overrides[getDB] = override_get_db
app.dependency_overrides[getCurrentUser] = override_get_current_user


def test_return_user(test_User):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "joelduran"
    assert response.json()["email"] == "joelduran@email.com"
    assert response.json()["firstName"] == "joel"
    assert response.json()["lastName"] == "duran"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "(111)-111-1111"


def test_change_password_success(test_User):
    response = client.put(
        "/user/password",
        json={"password": "testpassword", "newPassword": "newpassword"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_User):
    response = client.put(
        "/user/password",
        json={"password": "wrongpassword", "newPassword": "newpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_User):
    response = client.put("/user/phonenumber/2222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
