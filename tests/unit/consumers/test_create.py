import pytest
from fastapi import status
from uuid import uuid4
from unittest.mock import AsyncMock

from src.domains.consumers.repositories import ConsumerRepository


@pytest.mark.asyncio
async def test_create_consumer_success(client, mocker):
    mock_consumer = {"id": uuid4(), "name": "Test", "email": "test@example.com"}
    mocker.patch.object(ConsumerRepository, 'create_consumer', AsyncMock(
        return_value=mock_consumer
    )
    )

    response = client.post("/consumers/", json={
        "name": "Test",
        "email": "test@example.com"
    }
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_consumer_invalid_data(client):
    response = client.post("/consumers/", json={"name": "", "email": "invalid"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
