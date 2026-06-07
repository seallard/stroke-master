"""Shared test fixtures."""

import os

import psycopg
import pytest
import pytest_asyncio
from psycopg.rows import dict_row

TEST_DB_URL = (
    os.environ.get("TEST_DATABASE_URL")
    or os.environ.get("DATABASE_URL")
    or "postgresql://stroke:stroke@localhost:5432/stroke"
)


@pytest_asyncio.fixture
async def db_conn():
    """An async connection whose work is rolled back after each test.

    Assumes migrations have been applied to the target DB. Skips the test (rather than
    failing) when no database is reachable, so `pytest` stays green without infra locally.
    """
    try:
        conn = await psycopg.AsyncConnection.connect(
            TEST_DB_URL, row_factory=dict_row, autocommit=False, connect_timeout=3
        )
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"no test database reachable at {TEST_DB_URL}: {exc}")

    try:
        yield conn
    finally:
        await conn.rollback()
        await conn.close()
