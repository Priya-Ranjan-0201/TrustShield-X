import uuid
import pytest
import pytest_asyncio
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.database import get_db
from app.models import Base, Role

from sqlalchemy.pool import StaticPool

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed default roles
    async with TestingSessionLocal() as session:
        roles = [
            Role(id=uuid.UUID("00000000-0000-0000-0000-000000000001"), name="CITIZEN", description="Citizen access"),
            Role(id=uuid.UUID("00000000-0000-0000-0000-000000000002"), name="BUSINESS", description="Business access"),
            Role(id=uuid.UUID("00000000-0000-0000-0000-000000000003"), name="GOVERNMENT", description="Government access"),
            Role(id=uuid.UUID("00000000-0000-0000-0000-000000000004"), name="ADMIN", description="Admin access"),
        ]
        session.add_all(roles)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
