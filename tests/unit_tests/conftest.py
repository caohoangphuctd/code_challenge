from typing import Callable

import pytest
from async_asgi_testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import close_all_sessions, sessionmaker

from app.config import config
from app.database.models import BaseModel

from . import helpers


def create_session_override(session: AsyncSession) -> Callable[[], AsyncSession]:
    def create_session_() -> AsyncSession:  # type: ignore
        yield session

    return create_session_


@pytest.fixture
def engine():
    engine = create_engine(
        config.db.URI, **config.db.SQLALCHEMY_ENGINE_OPTIONS, future=True
    )
    yield engine
    engine.dispose()


@pytest.fixture
async def async_engine():
    engine = create_async_engine(
        config.db.ASYNC_DATABASE_URI, **config.db.SQLALCHEMY_ENGINE_OPTIONS, future=True
    )
    yield engine
    await engine.dispose()


@pytest.fixture
def reset_database(engine):
    close_all_sessions()
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)


@pytest.fixture
async def async_session(reset_database, async_engine):
    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        future=True,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with Session() as session_:
        yield session_


@pytest.fixture
def sync_session(reset_database, engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

    with Session() as session_:
        yield session_


@pytest.fixture
def records(async_session):
    async def _records(path: str):
        return await helpers.create_records(async_session, path)

    return _records


@pytest.fixture
def app(reset_database):
    from app.main import app

    yield app


@pytest.fixture
async def client(app, async_session):
    from app.database.depends import create_session

    async with TestClient(app) as client_:
        app.dependency_overrides[create_session] = create_session_override(
            async_session
        )
        yield client_
