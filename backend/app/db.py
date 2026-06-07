"""Async Postgres access: a psycopg 3 connection pool + aiosql-loaded plain SQL.

No ORM. SQL lives in ``app/sql/*.sql`` and is loaded as named query functions; call
them with an async connection borrowed from the pool.

Async semantics (aiosql ``apsycopg`` adapter):
- A multi-row ``-- name: foo`` query returns an **async generator** — iterate it::

      async with get_pool().connection() as conn:
          rows = [r async for r in queries.list_activities_for_user(conn, user_id=uid, limit=50)]

- A single-row ``-- name: foo^`` query returns an awaitable::

      activity = await queries.get_activity(conn, id=aid)
"""

from pathlib import Path

import aiosql
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

from .config import get_settings

SQL_DIR = Path(__file__).parent / "sql"

# "apsycopg" is aiosql's async psycopg 3 adapter (the plain "psycopg" adapter is sync).
# mandatory_parameters=False keeps the lighter `-- name: foo` style (params as kwargs)
# rather than requiring an explicit signature list.
queries = aiosql.from_path(SQL_DIR, "apsycopg", mandatory_parameters=False)

_pool: AsyncConnectionPool | None = None


def get_pool() -> AsyncConnectionPool:
    if _pool is None:
        raise RuntimeError("DB pool is not open; call open_pool() during startup")
    return _pool


async def open_pool() -> None:
    """Open the pool. Non-blocking: startup won't fail if Postgres isn't up yet."""
    global _pool
    settings = get_settings()
    _pool = AsyncConnectionPool(
        conninfo=settings.database_url,
        open=False,
        kwargs={"row_factory": dict_row},
    )
    await _pool.open()  # wait=False by default — fills in the background


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
