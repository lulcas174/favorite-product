from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductRating(BaseModel):
    rate: float
    count: int


class ProductDetails(BaseModel):
    id: int
    title: str
    price: float
    image: str
    rating: Optional[ProductRating] = None

    model_config = ConfigDict(from_attributes=True)


class PaginatedProductResponse(BaseModel):
    data: list[ProductDetails]
    total: int
    page: int
    page_size: int
    total_pages: int
