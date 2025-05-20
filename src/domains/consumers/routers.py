from sqlite3 import IntegrityError
from uuid import UUID
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    Security,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.consumers.services import ConsumerService
from src.infrastructure.services.productsService import ProductsService

from .schemas import (
    ConsumerCreate,
    ConsumerResponse,
    ConsumerUpdate,
    FavoriteCreate,
    PaginatedConsumerResponse,
)
from .repositories import ConsumerRepository, FavoriteRepository
from src.infrastructure.database import get_db
from src.infrastructure.security import get_current_user

router = APIRouter(
    prefix="/consumers",
    tags=["consumers"],
    dependencies=[Security(get_current_user, scopes=[])],
)


@router.post(
    "/",
    response_model=ConsumerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_consumer(
    consumer_data: ConsumerCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ConsumerRepository.create_consumer(consumer_data, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=PaginatedConsumerResponse)
async def list_consumers(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    page_size: int = Query(
        100,
        ge=1,
        le=1000,
        description="Number of items per page (max 1000)",
    ),
    db: AsyncSession = Depends(get_db),
):
    return await ConsumerService.list_with_favorites(db, page, page_size)


@router.get("/{consumer_id}", response_model=ConsumerResponse)
async def retrieve_consumer(
    consumer_id: str,
    db: AsyncSession = Depends(get_db),
):
    consumer = await ConsumerRepository.get_consumer_by_id(consumer_id, db)
    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumer not found",
        )
    return await ConsumerService.retrive_consumer(consumer)


@router.put("/{consumer_id}", response_model=ConsumerResponse)
async def update_consumer(
    consumer_id: str,
    update_data: ConsumerUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        updated = await ConsumerRepository.update_consumer(
            consumer_id,
            update_data.dict(exclude_unset=True),
            db,
        )
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consumer not found",
            )
        return await ConsumerService.retrive_consumer(updated)
    except ValueError as e:
        if "Consumer with this email already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        raise


@router.delete("/{consumer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_consumer(
    consumer_id: str,
    db: AsyncSession = Depends(get_db),
):
    deleted = await ConsumerRepository.delete_consumer(consumer_id, db)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumer not found",
        )


@router.post(
    "/{consumer_id}/favorites",
    status_code=status.HTTP_201_CREATED,
)
async def add_favorites(
    consumer_id: UUID,
    favorite_data: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
):
    consumer = await ConsumerRepository.get_consumer_by_id(consumer_id, db)
    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumer not found"
        )

    added = []
    already_exists = []
    not_found = []

    for product_id in favorite_data.product_ids:
        product = await ProductsService.get_product_by_id(product_id)
        if not product:
            not_found.append(product_id)
            continue

        existing = await FavoriteRepository.get_favorite_by_product(
            consumer_id,
            product_id,
            db
        )
        if existing:
            already_exists.append(product_id)
            continue

        try:
            await FavoriteRepository.create_favorite(
                consumer_id=consumer_id,
                product_id=product_id,
                db=db
            )
            added.append(product_id)
        except IntegrityError:
            await db.rollback()
            already_exists.append(product_id)

    return {
        "message": "Favorites added successfully",
        "added": added,
        "already_exists": already_exists,
        "not_found": not_found
    }


@router.patch(
    "/{consumer_id}/favorites/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_favorite(
    consumer_id: UUID,
    product_id: str,
    db: AsyncSession = Depends(get_db),
):
    if not product_id.isdigit():
        raise HTTPException(
            status_code=422,
            detail="Product ID must be a numeric value"
        )
    consumer = await ConsumerRepository.get_consumer_by_id(consumer_id, db)
    if not consumer:
        raise HTTPException(status_code=404, detail="Consumer not found")

    product_id_int = int(product_id)
    product = await ProductsService.get_product_by_id(product_id_int)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    favorite = await FavoriteRepository.get_favorite_by_product(
        consumer_id,
        product_id,
        db
    )
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    await FavoriteRepository.delete_favorite(favorite, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "update/favorites/{consumer_id}",
    status_code=status.HTTP_200_OK,
)
async def update_favorites(
    consumer_id: UUID,
    favorite_data: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
):
    consumer = await ConsumerRepository.get_consumer_by_id(consumer_id, db)
    if not consumer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consumer not found"
        )

    added = []
    already_exists = []
    not_found = []

    for product_id in favorite_data.product_ids:
        product = await ProductsService.get_product_by_id(product_id)
        if not product:
            not_found.append(product_id)
            continue

        existing = await FavoriteRepository.get_favorite_by_product(
            consumer_id,
            product_id,
            db
        )
        if existing:
            already_exists.append(product_id)
            continue

        try:
            await FavoriteRepository.create_favorite(
                consumer_id=consumer_id,
                product_id=product_id,
                db=db
            )
            added.append(product_id)
        except IntegrityError:
            await db.rollback()
            already_exists.append(product_id)

    return {
        "message": "Favorites updated successfully",
        "added": added,
        "already_exists": already_exists,
        "not_found": not_found
    }
