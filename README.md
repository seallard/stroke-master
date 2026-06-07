# stroke-master

Rowing analytics based on stroke, gps and weather data.

Ingests workouts from an NK SpeedCoach GPS 2 (via Strava), enriches them with weather,
and produces rowing-specific analytics. See [CLAUDE.md](./CLAUDE.md) for architecture and
design decisions.

## Layout

- `backend/` — FastAPI (async) + psycopg 3 plain SQL + arq worker
- `frontend/` — Vite + React + TypeScript
- `docker-compose.yml` — postgres + redis + api + worker + web for local dev

## Quickstart (Docker)

```bash
docker compose up --build
```

- API: http://localhost:8000 (docs at `/docs`, health at `/health`)
- Web: http://localhost:5173

The `api` service applies migrations (`yoyo apply`) on startup.

## Backend (without Docker)

Requires [uv](https://docs.astral.sh/uv/) and a running Postgres + Redis.

```bash
cd backend
cp .env.example .env            # fill in Strava + S3 creds as needed
uv sync                         # install deps
uv run yoyo apply               # apply migrations (uses yoyo.ini dev DSN)
uv run uvicorn app.main:app --reload   # API on :8000
uv run arq app.worker.WorkerSettings   # background worker
uv run pytest                   # tests
```

## Frontend (without Docker)

Requires **Node 18+** (the Docker `web` service uses node:20, so `docker compose` works
regardless of your host Node version).

```bash
cd frontend
npm install
npm run dev                     # Vite on :5173
```

## Git hooks (formatting + tests on commit)

Managed by [pre-commit](https://pre-commit.com/) — runs ruff (Python lint+format), Prettier
(frontend), and pytest before each commit. It provisions its own tool environments (including
its own Node for Prettier), so it works regardless of your host Node version.

```bash
uv tool install pre-commit   # or: pipx install pre-commit
pre-commit install           # activate the git hook (once per clone)
pre-commit run --all-files   # optional: run against the whole repo
```

## Status

Scaffold: app skeleton, DB schema/migrations, async DB layer, and stubbed routers/parsers
are in place. Next: implement Strava OAuth login and activity sync (see CLAUDE.md build order).
