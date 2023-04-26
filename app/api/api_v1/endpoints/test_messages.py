# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401
import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from app.main import app
from app.models import Topics

pytestmark = pytest.mark.anyio


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
async def client():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as c:
            yield c


async def test_receive_message(client: AsyncClient):  # nosec
    message = {"topic": "Question", "description": "I've got a question for you..."}
    response = await client.post("api/v1/message/", json=message)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "message" in data
