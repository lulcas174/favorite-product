from fastapi import APIRouter, Query, Security

from src.domains.products.schemas import PaginatedProductResponse
from src.domains.products.services import ProductService
from src.infrastructure.security import get_current_user

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Security(get_current_user, scopes=[])],
)


@router.get("", response_model=PaginatedProductResponse)
async def get_available_products(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    page_size: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of items per page (max 100)",
    ),
):
    return await ProductService.get_available_products(page, page_size)
