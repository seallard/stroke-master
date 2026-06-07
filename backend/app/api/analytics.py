"""Analytics endpoints. Serve precomputed aggregates (computed in the worker, cached);
do not crunch streams in the request path.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/activities/{activity_id}/summary")
async def activity_summary(activity_id: str) -> dict:
    # TODO: return derived aggregates for the activity.
    return {"todo": "activity summary", "activity_id": activity_id}
