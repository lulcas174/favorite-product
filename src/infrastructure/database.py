import importlib
import pathlib

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)

Base = declarative_base()


def load_all_models():
    base_path = pathlib.Path(__file__).resolve().parent.parent / "domains"
    module_base = "src.domains"

    for module in base_path.iterdir():
        if module.is_dir() and (module / "models.py").exists():
            importlib.import_module(f"{module_base}.{module.name}.models")


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
