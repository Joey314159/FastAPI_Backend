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
