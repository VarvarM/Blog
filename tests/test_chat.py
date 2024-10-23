from typing import AsyncIterator

import pytest, pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

# Предположим, что у вас есть такой файл core/models.py
from core.models import db_helper

# Импортируем ваше приложение FastAPI
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


@pytest.mark.asyncio
async def test_create_user(async_client):
    user_data = {
        "username": "testuser"
    }
    response = await async_client.post('/api/v1/users/create_user', json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]


@pytest.mark.asyncio
async def test_get_user(async_client):
    # Создаем пользователя для теста
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    create_response = await async_client.post('/users/create_user', json=user_data)
    user_id = create_response.json()["id"]  # Предполагается, что у пользователя есть поле id

    response = await async_client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]


@pytest.mark.asyncio
async def test_update_user(async_client):
    # Создаем пользователя для теста
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    create_response = await async_client.post('/users/create_user', json=user_data)
    user_id = create_response.json()["id"]

    update_data = {"username": "updateduser", "email": "updated@example.com"}
    response = await async_client.put(f'/users/{user_id}', json=update_data)
    assert response.status_code == 200
    assert response.json()["username"] == update_data["username"]


@pytest.mark.asyncio
async def test_delete_user(async_client):
    # Создаем пользователя для теста
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    create_response = await async_client.post('/users/create_user', json=user_data)
    user_id = create_response.json()["id"]

    response = await async_client.delete(f'/users/{user_id}')
    assert response.status_code == 204

    # Проверяем, что пользователь удален
    response = await async_client.get(f'/users/{user_id}')
    assert response.status_code == 404  # Предполагается, что пользователь не найден
