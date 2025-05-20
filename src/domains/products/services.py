from typing import Dict, Any

from src.infrastructure.services.productsService import ProductsService
from src.domains.products.schemas import ProductDetails


class ProductService:
    @staticmethod
    async def get_available_products(
        page: int, page_size: int
    ) -> Dict[str, Any]:
        products = await ProductsService.get_products()
        total = len(products)
        start = (page - 1) * page_size
        end = start + page_size
        slice_ = products[start:end]

        items = [
            ProductDetails(
                id=p["id"],
                title=p["title"],
                price=p["price"],
                image=p["image"],
                review=p.get("rating"),
            )
            for p in slice_
        ]
        total_pages = (total + page_size - 1) // page_size or 1
        return {
            "data": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }
