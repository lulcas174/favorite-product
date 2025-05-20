from uuid import uuid4
from fastapi import status
from unittest.mock import AsyncMock

import pytest

from src.domains.consumers.repositories import ConsumerRepository
from src.domains.consumers.services import ConsumerService
from src.domains.consumers.schemas import (
    ConsumerResponse, PaginatedConsumerResponse
)


def test_list_consumers_success(client, mocker):
    mock_page = PaginatedConsumerResponse(
        data=[],
        total=0,
        page=1,
        page_size=10,
        total_pages=1
    )
    mocker.patch.object(
        ConsumerService,
        'list_with_favorites',
        AsyncMock(return_value=mock_page)
    )
    response = client.get("/consumers/?page=1&page_size=10")
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    assert json_data['total'] == 0
    assert json_data['data'] == []


@pytest.mark.asyncio
async def test_retrieve_consumer_success(client, mocker):
    mock_consumer = ConsumerResponse(
        id=uuid4(),
        name="Test",
        email="test@example.com",
        favorites=[]
    )
    mocker.patch.object(
        ConsumerRepository,
        'get_consumer_by_id',
        AsyncMock(return_value=True)
    )
    mocker.patch.object(
        ConsumerService,
        'retrive_consumer',
        AsyncMock(return_value=mock_consumer)
    )
    response = client.get(f"/consumers/{mock_consumer.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(mock_consumer.id)


@pytest.mark.asyncio
async def test_retrieve_consumer_not_found(client, mocker):
    mocker.patch.object(
        ConsumerRepository,
        'get_consumer_by_id',
        AsyncMock(return_value=None)
    )
    response = client.get(f"/consumers/{uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
