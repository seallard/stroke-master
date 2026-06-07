"""API request/response schemas (Pydantic). Kept separate from domain models so the
wire format can evolve independently of storage/domain shapes.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ActivitySummary(BaseModel):
    id: UUID
    source: str
    name: str | None = None
    start_time: datetime
    distance_m: float | None = None
    elapsed_time_s: int | None = None
