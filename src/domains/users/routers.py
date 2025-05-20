from fastapi import APIRouter, Depends, HTTPException, status
from src.domains.users.services import UserService
from src.infrastructure.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.security import (
    create_access_token,
    get_password_hash,
)
from .schemas import (
    UserCreateRequest,
    LoginRequest,
    Token,
    UserResponse
)
from sqlalchemy import select
from .models import User

router = APIRouter(prefix="/auth", tags=["authentication"], dependencies=[])


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await UserService.authenticate_user(login_data.email,
                                               login_data.password,
                                               db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(str(user.id))
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    new_user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        is_active=True
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
