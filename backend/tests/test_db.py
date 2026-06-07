"""DB layer tests: schema + plain-SQL query functions. Uses the rolled-back db_conn
fixture, so it leaves no data behind. Auto-skips when no database is available.
"""


async def test_activity_roundtrip(db_conn):
    from app.db import queries

    uid = (
        await (await db_conn.execute("insert into users default values returning id")).fetchone()
    )["id"]
    await db_conn.execute(
        "insert into activities (user_id, source, external_id, sport, name, start_time, distance_m)"
        " values (%s, 'strava', '42', 'Rowing', 'Test piece', now(), 6000)",
        (uid,),
    )

    # multi-row query -> async generator
    rows = [r async for r in queries.list_activities_for_user(db_conn, user_id=uid, limit=10)]
    assert len(rows) == 1
    assert rows[0]["source"] == "strava"
    assert rows[0]["distance_m"] == 6000.0

    # single-row query (^) -> awaitable
    one = await queries.get_activity(db_conn, id=rows[0]["id"])
    assert one is not None
    assert one["name"] == "Test piece"
