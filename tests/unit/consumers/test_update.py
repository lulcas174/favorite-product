import pytest
from fastapi import status
from uuid import uuid4
from unittest.mock import AsyncMock

from src.domains.consumers.services import ConsumerService
from src.domains.consumers.repositories import ConsumerRepository
from src.domains.consumers.schemas import ConsumerResponse


@pytest.mark.asyncio
async def test_update_consumer_success(client, mocker):
    mock_updated = ConsumerResponse(
        id=uuid4(),
        name="Updated",
        email="updated@example.com",
        favorites=[]
    )
    mocker.patch.object(
        ConsumerRepository,
        'update_consumer',
        AsyncMock(return_value=True)
    )
    mocker.patch.object(
        ConsumerService,
        'retrive_consumer',
        AsyncMock(return_value=mock_updated)
    )
    payload = {"name": "Updated", "email": "updated@example.com"}
    response = client.put(f"/consumers/{mock_updated.id}", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == "Updated"


@pytest.mark.asyncio
async def test_update_consumer_not_found(client, mocker):
    mocker.patch.object(
        ConsumerRepository,
        'update_consumer',
        AsyncMock(return_value=None)
    )
    payload = {"name": "NoOne", "email": "noone@example.com"}
    response = client.put(f"/consumers/{uuid4()}", json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
