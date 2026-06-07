"""Ingestion triggers. Heavy work is enqueued to the worker, never run inline."""

from fastapi import APIRouter

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("/strava/sync")
async def sync_strava() -> dict:
    # TODO: enqueue an arq job to pull the user's recent rowing activities.
    return {"todo": "enqueue strava sync job"}


@router.post("/upload")
async def upload_file() -> dict:
    # TODO (later): accept NK CSV/FIT upload, enqueue parse job.
    return {"todo": "accept NK CSV/FIT upload"}
