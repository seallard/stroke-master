"""arq background worker. All ingestion and CPU-bound analytics run here, off the API
request path. Run with: ``uv run arq app.worker.WorkerSettings``.
"""

from arq.connections import RedisSettings

from ..config import get_settings


async def sync_strava_activity(ctx: dict, activity_external_id: str) -> None:
    """Pull a Strava activity, normalize, store the raw stream to object storage, persist
    metadata + derived aggregates. TODO: implement.
    """
    # from ..ingest import strava_sync
    # activity, samples = await strava_sync.fetch_and_map(token, activity_external_id)
    ...


class WorkerSettings:
    functions = [sync_strava_activity]
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
