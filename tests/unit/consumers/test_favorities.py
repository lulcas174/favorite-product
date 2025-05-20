from http import HTTPStatus
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

    mock_create = mocker.patch.object(
        FavoriteRepository,
        "create_favorite",
        AsyncMock(),
    )

    payload = {"product_ids": ["1"]}
    response = client.post(
        f"/consumers/{consumer_id}/favorites",
        json=payload,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "message": "Favorites added successfully",
        "added": ["1"],
        "already_exists": [],
        "not_found": [],
    }

    mock_create.assert_called_once_with(
        consumer_id=consumer_id,
        product_id="1",
        db=mock_create.call_args.kwargs["db"]
    )


@pytest.mark.asyncio
async def test_add_favorite_not_found_consumer(client, mocker):
    mocker.patch.object(
        ConsumerRepository,
        "get_consumer_by_id",
        AsyncMock(return_value=None),
    )

    response = client.post(
        f"/consumers/{uuid4()}/favorites",
        json={"product_ids": ["1", "2"]},
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
        json={"product_ids": ["105"]},
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "not_found" in data
    assert "105" in data["not_found"]


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
    mocker.patch.object(
        ProductsService,
        "get_product_by_id",
        AsyncMock(return_value=mock_product),
    )

    get_favorite_mock = AsyncMock()
    get_favorite_mock.side_effect = [None, None, object(), object()]
    mocker.patch.object(
        FavoriteRepository,
        "get_favorite_by_product",
        get_favorite_mock,
    )
    mocker.patch.object(
        FavoriteRepository,
        "create_favorite",
        AsyncMock(),
    )

    payload = {"product_ids": ["1", "2"]}

    first = client.post(
        f"/consumers/{consumer_id}/favorites",
        json=payload,
    )
    assert first.status_code == status.HTTP_201_CREATED
    first_json = first.json()
    assert len(first_json["added"]) == 2
    assert len(first_json["already_exists"]) == 0
    assert len(first_json["not_found"]) == 0

    second = client.post(
        f"/consumers/{consumer_id}/favorites",
        json=payload,
    )
    assert second.status_code == status.HTTP_201_CREATED
    second_json = second.json()
    assert len(second_json["added"]) == 0
    assert len(second_json["already_exists"]) == 2
    assert len(second_json["not_found"]) == 0


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
