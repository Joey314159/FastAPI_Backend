from .utils import *
from ..routers.Admin import getDB, getCurrentUser
from fastapi import status


app.dependency_overrides[getDB] = override_get_db
app.dependency_overrides[getCurrentUser] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
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
