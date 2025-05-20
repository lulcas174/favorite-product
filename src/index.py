from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from src.config.settings import Settings
from src.infrastructure.database import engine
from src.routers import main_router

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connection sucess!")
    except Exception as e:
        print("Erro to connect:", e)
    yield


app = FastAPI(
    title="API of favorite products",
    lifespan=lifespan,
    swagger_ui_parameters={"docExpansion": "none"},
    # dependencies=[Depends(security_scheme)]
)

app.include_router(main_router)
