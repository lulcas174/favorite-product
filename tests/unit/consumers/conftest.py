import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.domains.consumers.routers import router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)

    async def mock_get_current_user():
        return {"user": "test-user"}

    dependency = router.dependencies[0].dependency
    app.dependency_overrides[dependency] = mock_get_current_user
    return TestClient(app)
