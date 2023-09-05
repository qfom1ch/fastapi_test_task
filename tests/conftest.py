import asyncio
from datetime import datetime
from typing import Any, Generator

import asyncpg
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from starlette.testclient import TestClient

from config import TEST_DATABASE_URL
from db.session import Base, get_db
from main import app

CLEAN_TABLES = [
    "orders",
    "customers",
    "stores_mtm_workers",
    "workers",
    "stores",
]


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def async_test_engine():
    async_test_engine = create_async_engine(TEST_DATABASE_URL,
                                            future=True,
                                            echo=False,
                                            execution_options={
                                                "isolation_level":
                                                    "AUTOCOMMIT"})
    yield async_test_engine


@pytest.fixture(scope="session", autouse=True)
async def async_session_test(async_test_engine):
    async_session = sessionmaker(bind=async_test_engine,
                                 expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope='session', autouse=True)
async def prepare_database(async_test_engine):
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(
                    text(f"DELETE FROM {table_for_cleaning};"))


async def get_test_db() -> Generator:
    try:
        async_test_engine = create_async_engine(TEST_DATABASE_URL,
                                                future=True,
                                                echo=False,
                                                execution_options={
                                                    "isolation_level":
                                                        "AUTOCOMMIT"}
                                                )

        async_test_session = sessionmaker(bind=async_test_engine,
                                          expire_on_commit=False,
                                          class_=AsyncSession)
        session: AsyncSession = async_test_session()
        yield session
    finally:
        await session.close()


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    await pool.close()


@pytest.fixture
async def create_worker_in_database(asyncpg_pool):
    async def create_worker_in_database(
            id: int,
            name: str,
            phone: str
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                "INSERT INTO workers VALUES ($1, $2, $3)",
                id,
                name,
                phone
            )

    return create_worker_in_database


@pytest.fixture
async def create_store_in_database(asyncpg_pool):
    async def create_store_in_database(
            id: int,
            name: str
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                "INSERT INTO stores VALUES ($1, $2)",
                id,
                name
            )

    return create_store_in_database


@pytest.fixture
async def create_store_mtm_workers(asyncpg_pool):
    async def create_store_mtm_workers(
            id: int,
            stores_id: int,
            workers_id: int
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                "INSERT INTO stores_mtm_workers VALUES ($1, $2, $3)",
                id,
                stores_id,
                workers_id
            )

    return create_store_mtm_workers


@pytest.fixture
async def create_customer_in_database(asyncpg_pool):
    async def create_customer_in_database(
            id: int,
            name: str,
            phone: str,
            store_id: int
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                "INSERT INTO customers VALUES ($1, $2, $3, $4)",
                id,
                name,
                phone,
                store_id
            )

    return create_customer_in_database


@pytest.fixture
async def create_order_in_database(asyncpg_pool):
    async def create_order_in_database(
            id: int,
            creation_time: datetime,
            end_time: datetime,
            store_id: int,
            author_id: int,
            status: str,
            executor_id: int
    ):
        async with asyncpg_pool.acquire() as connection:
            return await connection.execute(
                "INSERT INTO orders VALUES ($1, $2, $3, $4, $5, $6, $7)",
                id,
                creation_time,
                end_time,
                store_id,
                author_id,
                status,
                executor_id,
            )

    return create_order_in_database


@pytest.fixture
async def get_order_from_database(asyncpg_pool):
    async def get_order_from_database_by_id(order_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch(
                "SELECT * FROM orders WHERE id = $1;", order_id
            )

    return get_order_from_database_by_id
