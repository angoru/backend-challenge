from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_send_email():
    response = client.post(
        "/api/v1/message/",
        json={"topic": "Sales", "description": "This is a bot message"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "email has been sent"}
