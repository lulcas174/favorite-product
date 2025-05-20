from sqlalchemy.ext.asyncio import AsyncSession
from src.domains.consumers.models import Consumer
from src.domains.consumers.repositories import ConsumerRepository
from src.infrastructure.services.productsService import ProductsService
from src.domains.consumers.schemas import (
    ConsumerResponse,
    PaginatedConsumerResponse
)


class ConsumerService:
    @staticmethod
    async def list_with_favorites(
        db: AsyncSession, page: int, page_size: int
    ) -> PaginatedConsumerResponse:
        total = await ConsumerRepository.count_consumers(db)
        consumers = await ConsumerRepository.get_all_consumers_with_favorites(
            db,
            skip=(page - 1) * page_size,
            limit=page_size
        )

        favorite_ids = {
            fav.product_id
            for consumer in consumers
            for fav in consumer.favorites
        }

        products_map = {}
        for product_id in favorite_ids:
            product = await ProductsService.get_product_by_id(product_id)
            if product:
                products_map[str(product_id)] = product

        return PaginatedConsumerResponse(
            data=[
                ConsumerResponse.from_domain(c, products_map)
                for c in consumers
            ],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size or 1,
        )

    @staticmethod
    async def retrive_consumer(consumer: Consumer) -> ConsumerResponse:
        products_map = {}
        for fav in consumer.favorites:
            product = await ProductsService.get_product_by_id(fav.product_id)
            if product:
                products_map[str(fav.product_id)] = product

        return ConsumerResponse.from_domain(consumer, products_map)
