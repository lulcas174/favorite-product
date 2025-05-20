import pytest
from fastapi import FastAPI, HTTPException, status
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from src.domains.products.routers import router
from src.domains.products.schemas import ProductDetails
from src.domains.products.services import ProductService
from src.infrastructure.services.productsService import ProductsService


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)

    async def mock_get_current_user():
        return {"user": "test-user"}

    app.dependency_overrides[
        router.dependencies[0].dependency
    ] = mock_get_current_user
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_available_products_success(mocker):
    mock_products = [
        {
            "id": i,
            "title": f"Product {i}",
            "price": i * 10,
            "image": f"image_{i}.jpg",
            "rating": {"rate": 4.5},
        }
        for i in range(1, 21)
    ]
    mocker.patch.object(
        ProductsService, 'get_products', AsyncMock(return_value=mock_products)
    )

    result = await ProductService.get_available_products(page=2, page_size=5)

    assert result["total"] == 20
    assert result["page"] == 2
    assert result["page_size"] == 5
    assert result["total_pages"] == 4
    assert len(result["data"]) == 5
    assert isinstance(result["data"][0], ProductDetails)
    assert result["data"][0].id == 6


@pytest.mark.asyncio
async def test_pagination_edge_cases(mocker):
    mock_products = [
        {"id": 1, "title": "Product 1", "price": 10, "image": "image1.jpg"}
    ]
    mocker.patch.object(
        ProductsService, 'get_products', AsyncMock(return_value=mock_products)
    )

    result = await ProductService.get_available_products(page=2, page_size=10)
    assert result["data"] == []
    assert result["total_pages"] == 1

    result = await ProductService.get_available_products(page=1, page_size=100)
    assert len(result["data"]) == 1


@pytest.mark.asyncio
async def test_service_error_handling(mocker):
    mocker.patch.object(
        ProductsService,
        'get_products',
        AsyncMock(side_effect=HTTPException(500, "Erro interno")),
    )

    with pytest.raises(HTTPException) as exc:
        await ProductService.get_available_products(1, 10)

    assert exc.value.status_code == 500


def test_route_validation(client):
    response = client.get("/products?page=0&page_size=5")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = client.get("/products?page=1&page_size=101")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_route_success(client, mocker):
    mock_data = {
        "data": [],
        "total": 0,
        "page": 1,
        "page_size": 10,
        "total_pages": 1,
    }

    mocker.patch.object(
        ProductService,
        'get_available_products',
        AsyncMock(return_value=mock_data),
    )

    response = client.get("/products?page=1&page_size=10")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_data


def test_unauthorized_access():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    response = client.get("/products")
    assert response.status_code == status.HTTP_403_FORBIDDEN
