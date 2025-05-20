from fastapi import HTTPException
import httpx


class ProductsService:
    @staticmethod
    async def get_products() -> list:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get("https://fakestoreapi.com/products")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error fetching products: {str(e)}",
                )
            except httpx.RequestError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Connection error: {str(e)}",
                )

    @staticmethod
    async def get_product_by_id(product_id: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"https://fakestoreapi.com/products/{product_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise HTTPException(
                    status_code=500,
                    detail=f"Error fetching product: {str(e)}"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Connection error: {str(e)}"
                )
