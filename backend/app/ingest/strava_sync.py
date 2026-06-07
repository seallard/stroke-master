"""Strava ingestion: OAuth token refresh + pull activities/streams → canonical model.

Filters to rowing activity types only. Built first (the POC path).
"""

from ..models import Activity, Sample

STRAVA_API = "https://www.strava.com/api/v3"
ROWING_SPORT_TYPES = {"Rowing", "VirtualRow", "Kayaking", "Canoeing"}


async def fetch_and_map(
    access_token: str, activity_external_id: str
) -> tuple[Activity, list[Sample]]:
    """Pull one Strava activity + its streams and map to the canonical model.

    TODO: GET /activities/{id} and /activities/{id}/streams (time, latlng, distance,
    velocity_smooth, heartrate, cadence), then build Activity + Sample[].
    """
    raise NotImplementedError
