import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from fastapi import status

from src.domains.consumers.repositories import (
    ConsumerRepository,
    FavoriteRepository
)
from src.infrastructure.services.productsService import ProductsService


@pytest.mark.asyncio
async def test_add_favorite_success(client, mocker):
    consumer_id = uuid4()
    mock_consumer = object()
    mock_product = {
        "id": "1",
        "title": "Prod",
        "price": 10.0,
        "image": "url",
    }

    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=mock_consumer),
    )
    mocker.patch.object(
        ProductsService,
        "get_product_by_id",
        AsyncMock(return_value=mock_product),
    )
    mocker.patch.object(
        FavoriteRepository,
        "get_favorite_by_product",
        AsyncMock(return_value=None),
    )
    mocker.patch.object(
        FavoriteRepository,
        "create_favorite",
        AsyncMock(),
    )

    payload = {"product_id": "1"}
    response = client.post(
        f"/consumers/{consumer_id}/favorites",
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "Favorite added successfully",
        "product_id": "1",
    }


@pytest.mark.asyncio
async def test_add_favorite_not_found_consumer(client, mocker):
    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=None),
    )

    response = client.post(
        f"/consumers/{uuid4()}/favorites",
        json={"product_id": "1"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_add_favorite_not_found_product(client, mocker):
    consumer_id = uuid4()

    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=object()),
    )
    mocker.patch.object(
        ProductsService,
        "get_product_by_id",
        AsyncMock(return_value=None),
    )

    response = client.post(
        f"/consumers/{consumer_id}/favorites",
        json={"product_id": "1"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_add_favorite_already_exists(client, mocker):
    consumer_id = uuid4()
    mock_consumer = object()
    mock_product = {"id": "1", "title": "Prod", "price": 10.0, "image": "url"}

    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=mock_consumer),
    )
    prod_side_effect = AsyncMock(side_effect=[mock_product, mock_product])
    mocker.patch.object(
        ProductsService,
        "get_product_by_id",
        prod_side_effect,
    )
    fav_side_effect = AsyncMock(side_effect=[None, object()])
    mocker.patch.object(
        FavoriteRepository,
        "get_favorite_by_product",
        fav_side_effect,
    )
    mocker.patch.object(
        FavoriteRepository,
        "create_favorite",
        AsyncMock(),
    )

    payload = {"product_id": "1"}
    first = client.post(
        f"/consumers/{consumer_id}/favorites",
        json=payload,
    )
    assert first.status_code == status.HTTP_201_CREATED

    second = client.post(
        f"/consumers/{consumer_id}/favorites",
        json=payload,
    )
    assert second.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_remove_favorite_success(client, mocker):
    consumer_id = uuid4()
    product_id = "1"
    mock_consumer = object()
    mock_fav = object()
    mock_product = {"id": "1", "title": "Prod", "price": 10.0, "image": "url"}

    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=mock_consumer),
    )
    mocker.patch.object(
        ProductsService,
        "get_product_by_id",
        AsyncMock(return_value=mock_product),
    )
    mocker.patch.object(
        FavoriteRepository,
        "get_favorite_by_product",
        AsyncMock(return_value=mock_fav),
    )
    mocker.patch.object(
        FavoriteRepository,
        "delete_favorite",
        AsyncMock(),
    )

    response = client.patch(
        f"/consumers/{consumer_id}/favorites/{product_id}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_remove_favorite_invalid_id(client):
    response = client.patch(
        f"/consumers/{uuid4()}/favorites/abc",
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_remove_favorite_not_found_consumer(client, mocker):
    consumer_id = uuid4()
    product_id = "1"

    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=None),
    )

    response = client.patch(
        f"/consumers/{consumer_id}/favorites/{product_id}",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_remove_favorite_not_found_product(client, mocker):
    consumer_id = uuid4()
    product_id = "1"

    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=object()),
    )
    mocker.patch.object(
        ProductsService,
        "get_product_by_id",
        AsyncMock(return_value=None),
    )

    response = client.patch(
        f"/consumers/{consumer_id}/favorites/{product_id}",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_remove_favorite_not_found_favorite(client, mocker):
    consumer_id = uuid4()
    product_id = "1"

    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=object()),
    )
    mocker.patch.object(
        ProductsService,
        "get_product_by_id",
        AsyncMock(return_value={}),
    )
    mocker.patch.object(
        FavoriteRepository,
        "get_favorite_by_product",
        AsyncMock(return_value=None),
    )

    response = client.patch(
        f"/consumers/{consumer_id}/favorites/{product_id}",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
