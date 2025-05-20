import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock, AsyncMock
from src.index import app
from src.infrastructure.database import get_db


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, mocker):
    mock_db = AsyncMock()
    mock_user = MagicMock()
    mock_user.id = 123
    authenticate_user_mock = AsyncMock(return_value=mock_user)
    mocker.patch(
        "src.domains.users.services.UserService.authenticate_user",
        new=authenticate_user_mock
    )

    mocker.patch(
        "src.infrastructure.security.create_access_token",
        return_value="token_acesso"
    )

    app.dependency_overrides[get_db] = lambda: mock_db

    login_data = {"email": "user@example.com", "password": "senhaCorreta"}
    response = await async_client.post("api/v1/auth/login", json=login_data)

    assert response.status_code == 200

    authenticate_user_mock.assert_awaited_once_with(
        login_data["email"], login_data["password"], mock_db
    )
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_failed(async_client: AsyncClient, mocker):
    mock_db = AsyncMock()
    authenticate_user_mock = AsyncMock(return_value=None)
    mocker.patch(
        "src.domains.users.services.UserService.authenticate_user",
        new=authenticate_user_mock
    )
    app.dependency_overrides[get_db] = lambda: mock_db
    login_data = {"email": "user@example.com", "password": "senhaIncorreta"}
    response = await async_client.post("api/v1/auth/login", json=login_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Incorrect email or password"}

    authenticate_user_mock.assert_awaited_once_with(
        login_data["email"], login_data["password"], mock_db
    )
    app.dependency_overrides.clear()
