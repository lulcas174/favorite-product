from sqlalchemy import select
from src.domains.users.models import User
from src.infrastructure.database import get_db
from src.infrastructure.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    @staticmethod
    async def create_user(user_data):
        async with get_db() as db:
            existing_user = await UserRepository.get_user_by_email(user_data.email)
            if existing_user:
                raise ValueError("User already exists")

            hashed_password = get_password_hash(user_data.password)
            new_user = User(
                email=user_data.email,
                hashed_password=hashed_password,
            )
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return new_user

    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession):
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()
