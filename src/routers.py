from fastapi import APIRouter
from src.domains.users.routers import router as users_router
from src.domains.consumers.routers import router as consumer_router
from src.domains.products.routers import router as product_router

main_router = APIRouter()

main_router.include_router(users_router, prefix="/api/v1")
main_router.include_router(consumer_router, prefix="/api/v1")
main_router.include_router(product_router, prefix="/api/v1")
