from typing import Mapping
import uuid

from pydantic import BaseModel, Field

from src.domains.consumers.models import Consumer
from src.domains.products.schemas import ProductDetails


class ConsumerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., description="Consumer email")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Nome muito sinistro",
                "email": "emailForteDoCliente@example.com",
            }]
        }
    }


class ConsumerCreate(ConsumerBase):
    pass


class ConsumerUpdate(ConsumerBase):
    pass


class ConsumerResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    favorites: list[ProductDetails] = []

    @classmethod
    def from_domain(
        cls, consumer: Consumer, products_map: Mapping[str, dict]
    ) -> "ConsumerResponse":
        favs = [
            ProductDetails(**products_map[fav.product_id])
            for fav in consumer.favorites
            if fav.product_id in products_map
        ]
        return cls(
            id=consumer.id,
            name=consumer.name,
            email=consumer.email,
            favorites=favs
        )


class FavoriteCreate(BaseModel):
    product_id: str = Field(..., min_length=1)


class PaginatedConsumerResponse(BaseModel):
    data: list[ConsumerResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
