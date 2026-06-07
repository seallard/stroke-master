"""Strava OAuth login.

Login = connecting Strava. The callback exchanges the code, then finds-or-creates the
``User`` for that Strava athlete (identity stays decoupled from Strava — see CLAUDE.md).
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/strava/login")
async def strava_login() -> dict:
    # TODO: build Strava authorize URL and redirect (scope: read,activity:read_all).
    return {"todo": "redirect to Strava OAuth authorize URL"}


@router.get("/strava/callback")
async def strava_callback(code: str | None = None, error: str | None = None) -> dict:
    # TODO: exchange `code` for tokens, find-or-create User + StravaConnection,
    #       establish a session signed with SECRET_KEY.
    return {"todo": "handle OAuth callback", "code": code, "error": error}
