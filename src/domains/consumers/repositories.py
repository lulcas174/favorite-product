import datetime
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.domains.consumers.models import Consumer, Favorite


class ConsumerRepository:
    @staticmethod
    async def create_consumer(consumer_data, db: AsyncSession):
        existing_consumer = (
            await ConsumerRepository.get_consumer_by_email(
                consumer_data.email,
                db,
            )
        )
        if existing_consumer:
            raise ValueError("Consumer with this email already exists")

        new_consumer = Consumer(
            name=consumer_data.name,
            email=consumer_data.email,
            favorites=[],
        )
        db.add(new_consumer)
        await db.commit()
        await db.refresh(new_consumer)
        return new_consumer

    @staticmethod
    async def get_consumer_by_email(email: str, db: AsyncSession):
        result = await db.execute(
            select(Consumer).filter(Consumer.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_consumer_by_id(consumer_id: str, db: AsyncSession):
        result = await db.execute(
            select(Consumer)
            .options(selectinload(Consumer.favorites))
            .filter(Consumer.id == consumer_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_consumer(
        consumer_id: str,
        update_data: dict,
        db: AsyncSession,
    ):
        consumer = await ConsumerRepository.get_consumer_by_id(
            consumer_id,
            db,
        )
        if not consumer:
            return None
        if 'email' in update_data and update_data['email'] is not None:
            existing_consumer = await ConsumerRepository.get_consumer_by_email(
                update_data["email"],
                db,
            )
            if existing_consumer and existing_consumer.id != consumer_id:
                raise ValueError("Consumer with this email already exists")

        for key, value in update_data.items():
            if value is not None:
                setattr(consumer, key, value)

        await db.commit()
        await db.refresh(consumer)
        return consumer

    @staticmethod
    async def delete_consumer(consumer_id: str, db: AsyncSession):
        consumer = await ConsumerRepository.get_consumer_by_id(
            consumer_id,
            db,
        )
        if not consumer:
            return None

        await db.delete(consumer)
        await db.commit()
        return consumer

    @staticmethod
    async def get_all_consumers_with_favorites(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ):
        result = await db.execute(
            select(Consumer)
            .options(selectinload(Consumer.favorites))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def count_consumers(db: AsyncSession):
        result = await db.execute(select(func.count(Consumer.id)))
        return result.scalar_one()


class FavoriteRepository:
    @staticmethod
    async def create_favorite(
        consumer_id: UUID,
        product_id: str,
        db: AsyncSession
    ):
        favorite = Favorite(
            consumer_id=consumer_id,
            product_id=product_id,
            created_at=datetime.datetime.utcnow()
        )
        db.add(favorite)
        await db.commit()
        await db.refresh(favorite)
        return favorite

    @staticmethod
    async def get_favorite_by_product(
        consumer_id: UUID,
        product_id: str,
        db: AsyncSession,
    ):
        result = await db.execute(
            select(Favorite).where(
                (
                    (Favorite.consumer_id == consumer_id)
                    & (Favorite.product_id == product_id)
                )
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_favorites_by_consumer_id(consumer_id: UUID, db: AsyncSession):
        result = await db.execute(
            select(Favorite).where(Favorite.consumer_id == consumer_id)
        )
        return result.scalars().all()

    @staticmethod
    async def delete_favorite(favorite: Favorite, db: AsyncSession):
        await db.delete(favorite)
        await db.commit()
