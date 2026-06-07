"""Strava webhook: subscription validation (GET) + event receiver (POST).

Push-based ingestion is the scalable path — Strava's rate limit is per-application, so
polling many athletes doesn't scale.
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from ..config import get_settings

router = APIRouter(prefix="/webhooks/strava", tags=["webhooks"])


@router.get("")
async def verify(request: Request):
    """Strava subscription handshake: echo hub.challenge when the verify token matches."""
    params = request.query_params
    if params.get("hub.verify_token") == get_settings().strava_webhook_verify_token:
        return JSONResponse({"hub.challenge": params.get("hub.challenge")})
    return JSONResponse({"error": "invalid verify token"}, status_code=403)


@router.post("")
async def receive(request: Request):
    _event = await request.json()
    # TODO: for activity create/update events, enqueue an arq pull for _event["object_id"].
    # Respond fast (200) so Strava doesn't retry.
    return JSONResponse({"status": "received"})
