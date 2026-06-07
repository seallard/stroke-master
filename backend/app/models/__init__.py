"""Canonical domain models (Pydantic). Source-agnostic — every ingest parser emits these.

Note: ``Sample`` is the in-memory/object-storage shape, not a Postgres table. Raw sample
streams are stored in object storage; Postgres holds User/StravaConnection/Activity rows
plus derived aggregates.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    email: str | None = None
    created_at: datetime


class StravaConnection(BaseModel):
    id: UUID
    user_id: UUID
    athlete_id: int
    expires_at: datetime
    scope: str | None = None


class Activity(BaseModel):
    id: UUID | None = None
    user_id: UUID
    source: str  # "strava" | "nk_csv" | "nk_fit"
    external_id: str | None = None
    sport: str | None = None
    name: str | None = None
    start_time: datetime
    elapsed_time_s: int | None = None
    distance_m: float | None = None
    start_lat: float | None = None
    start_lng: float | None = None
    stream_object_key: str | None = None


class Sample(BaseModel):
    t: float  # seconds from activity start
    lat: float | None = None
    lng: float | None = None
    distance_m: float | None = None
    speed_mps: float | None = None
    stroke_rate_spm: float | None = None
    heart_rate: int | None = None
