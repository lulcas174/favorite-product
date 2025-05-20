import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock, AsyncMock
from src.index import app
from src.infrastructure.database import get_db


@pytest.mark.asyncio
async def test_register_success(async_client: AsyncClient, mocker):
    mock_session = AsyncMock()
    mock_session.execute.return_value = MagicMock(
        scalars=MagicMock(return_value=MagicMock(
            first=MagicMock(
                return_value=None)))
    )

    app.dependency_overrides[get_db] = lambda: mock_session

    test_data = {"email": "new@example.com", "password": "senhaSegura123"}
    response = await async_client.post("api/v1/auth/register", json=test_data)

    assert response.status_code == 201
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_register_email_exists(async_client: AsyncClient, mocker):
    mock_session = AsyncMock()
    mock_execute_result = MagicMock()
    mock_execute_result.scalars.return_value.first.return_value = MagicMock()
    mock_session.execute.return_value = mock_execute_result

    app.dependency_overrides[get_db] = lambda: mock_session

    test_data = {"email": "existente@example.com", "password": "outraSenha"}
    response = await async_client.post("api/v1/auth/register", json=test_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"
    mock_session.add.assert_not_called()
    app.dependency_overrides.clear()
