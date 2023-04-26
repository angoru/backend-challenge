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


# async def test_create_topic(client: AsyncClient):  # nosec
#     response = await client.post(
#         "api/v1/topics/",
#         json={"name": "test", "plugin_class": "Class"},
#     )
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["name"] == "test"


async def test_list_channels(client: AsyncClient):  # nosec
    response = await client.get("api/v1/topics/")
    assert response.status_code == 200, response.text
