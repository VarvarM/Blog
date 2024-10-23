import pytest
from httpx import ASGITransport, AsyncClient
from main import app


@pytest.mark.asyncio
async def test_users():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/users")
        assert response.status_code == 200
        assert len(response.json()) == 4


@pytest.mark.asyncio
async def test_one_user():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/api/v1/users/5")
        assert response.status_code == 200
        assert response.json() == {"username": "kik",
                                   "id": 5}
