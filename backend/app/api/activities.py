"""Activity listing / detail endpoints."""

from fastapi import APIRouter

from ..schemas import ActivitySummary

router = APIRouter(prefix="/activities", tags=["activities"])


@router.get("", response_model=list[ActivitySummary])
async def list_activities() -> list[ActivitySummary]:
    # TODO: scope to the authenticated user; read via queries.list_activities_for_user.
    return []
