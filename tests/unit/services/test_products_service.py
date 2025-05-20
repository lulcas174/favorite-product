import pytest
from fastapi import HTTPException
import httpx
from unittest.mock import AsyncMock, MagicMock

from src.infrastructure.services.productsService import ProductsService


@pytest.mark.asyncio
async def test_get_products_success(mocker):
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": 1, "title": "Test Product"}]
    mock_response.raise_for_status = MagicMock()

    mock_client_instance.get.return_value = mock_response

    result = await ProductsService.get_products()

    assert result == [{"id": 1, "title": "Test Product"}]
    mock_client_instance.get.assert_called_once_with(
        "https://fakestoreapi.com/products"
    )
    mock_response.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_get_products_http_error(mocker):
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance

    http_error = httpx.HTTPStatusError(
        "Server error",
        request=httpx.Request("GET", "https://fakestoreapi.com/products"),
        response=httpx.Response(500)
    )

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = http_error
    mock_client_instance.get.return_value = mock_response

    with pytest.raises(HTTPException) as exc_info:
        await ProductsService.get_products()

    assert exc_info.value.status_code == 500
    assert "Error fetching products" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_products_connection_error(mocker):
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance

    mock_client_instance.get.side_effect = httpx.RequestError("Connection error")

    with pytest.raises(HTTPException) as exc_info:
        await ProductsService.get_products()

    assert exc_info.value.status_code == 500
    assert "Connection error" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_product_by_id_success(mocker):
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "1", "title": "Test Product"}
    mock_response.raise_for_status = MagicMock()

    mock_client_instance.get.return_value = mock_response

    result = await ProductsService.get_product_by_id("1")

    assert result == {"id": "1", "title": "Test Product"}
    mock_client_instance.get.assert_called_once_with(
        "https://fakestoreapi.com/products/1"
    )
    mock_response.raise_for_status.assert_called_once()


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(mocker):
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance

    http_error = httpx.HTTPStatusError(
        "Not found",
        request=httpx.Request("GET", "https://fakestoreapi.com/products/1"),
        response=httpx.Response(404)
    )

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = http_error
    mock_client_instance.get.return_value = mock_response

    result = await ProductsService.get_product_by_id("1")

    assert result is None


@pytest.mark.asyncio
async def test_get_product_by_id_http_error(mocker):
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance

    http_error = httpx.HTTPStatusError(
        "Server error",
        request=httpx.Request("GET", "https://fakestoreapi.com/products/1"),
        response=httpx.Response(500)
    )

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = http_error
    mock_client_instance.get.return_value = mock_response

    with pytest.raises(HTTPException) as exc_info:
        await ProductsService.get_product_by_id("1")

    assert exc_info.value.status_code == 500
    assert "Error fetching product" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_product_by_id_connection_error(mocker):
    mock_client = mocker.patch('httpx.AsyncClient')
    mock_client_instance = AsyncMock()
    mock_client.return_value.__aenter__.return_value = mock_client_instance

    mock_client_instance.get.side_effect = httpx.RequestError("Connection failed")

    with pytest.raises(HTTPException) as exc_info:
        await ProductsService.get_product_by_id("1")

    assert exc_info.value.status_code == 500
    assert "Connection error" in exc_info.value.detail
