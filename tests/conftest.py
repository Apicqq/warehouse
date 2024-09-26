from pathlib import Path

from fastapi.testclient import TestClient
from mixer.backend.sqlalchemy import Mixer as _mixer
import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.db import Base, get_async_session
from app.main import app

BASE_DIR = Path(__file__).resolve().parent.parent

TEST_DB = BASE_DIR / "test.db"
SQLALCHEMY_DB_URL = f"sqlite+aiosqlite:///{str(TEST_DB)}"
engine = create_async_engine(SQLALCHEMY_DB_URL)

TestingSession = async_sessionmaker(engine)


async def get_async_testing_session() -> TestingSession:
    async with TestingSession() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def mixer():
    mixer_engine = create_engine(f"sqlite:///{str(TEST_DB)}")
    session = sessionmaker(bind=mixer_engine)
    return _mixer(session=session(), commit=True)


@pytest.fixture
def client():
    app.dependency_overrides = {
        get_async_session: get_async_testing_session
    }
    with TestClient(app) as client:
        yield client


pytest_plugins = [
    "tests.fixtures.orders",
    "tests.fixtures.products",
]
