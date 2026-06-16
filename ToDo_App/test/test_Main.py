from fastapi.testclient import TestClient
from ..Main import app
from fastapi import status
# from typing import assert_type

client = TestClient(app)


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
