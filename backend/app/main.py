"""FastAPI application entrypoint (async, stateless)."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import activities, analytics, auth, ingest, strava_webhook
from .db import close_pool, open_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await open_pool()
    try:
        yield
    finally:
        await close_pool()


app = FastAPI(title="stroke-master", version="0.1.0", lifespan=lifespan)

# Dev CORS: allow the Vite frontend. Tighten/derive from settings for prod.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(activities.router)
app.include_router(ingest.router)
app.include_router(analytics.router)
app.include_router(strava_webhook.router)
