import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_login_success(async_client: AsyncClient):
    response = await async_client.post(
        "/login",
        json={"username": "test", "password": "test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

async def test_login_failure(async_client: AsyncClient):
    response = await async_client.post(
        "/login",
        json={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == 200  # Currently always returns 200, might want to change this
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Invalid credentials"

async def test_login_validation(async_client: AsyncClient):
    # Test missing username
    response = await async_client.post(
        "/login",
        json={"password": "test"}
    )
    assert response.status_code == 422

    # Test missing password
    response = await async_client.post(
        "/login",
        json={"username": "test"}
    )
    assert response.status_code == 422

    # Test empty payload
    response = await async_client.post(
        "/login",
        json={}
    )
    assert response.status_code == 422 