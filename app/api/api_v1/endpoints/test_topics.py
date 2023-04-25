from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_send_email():
    response = client.get("/api/v1/topics/")
    assert response.status_code == 200
