from typing import AsyncIterator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
# Импортируем ваше приложение FastAPI
from sqlalchemy.ext.asyncio import async_session, AsyncSession

from main import app


# Фикстура для создания асинхронного клиента
@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


# Тест для получения информации об одном пользователе
@pytest.mark.asyncio
async def test_one_user(async_client: AsyncClient):
    # Внутри теста мы ожидаем завершения асинхронного запроса
    response = await async_client.get("/api/v1/users/5")
    assert response.status_code == 200
    assert response.json() == {"username": "kik", "id": 5}


# Тест для получения списка всех пользователей
@pytest.mark.asyncio
async def test_users(async_client: AsyncClient):
    response = await async_client.get("/api/v1/users")
    assert response.status_code == 200
    assert len(response.json()) == 4
