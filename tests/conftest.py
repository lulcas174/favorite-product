import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from src.index import app


@pytest_asyncio.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver"
    ) as client:
        yield client
