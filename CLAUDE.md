# stroke-master

Rowing analytics web app. Ingests workouts recorded on an **NK SpeedCoach GPS 2**,
enriches them with **historical weather**, and produces rowing-specific analytics
(stroke rate, split, distance-per-stroke, pace/efficiency curves, environmental
correlation, and cross-session trends).

Each user analyzes only their own data — a per-athlete privacy boundary, not a scale assumption.

## Architecture & scaling

Designed to scale to a large (eventually global) user base. The current small user count must
**not** drive design decisions. Guiding rule: get the architectural **seams** right now (they
are expensive to retrofit), and defer only **operational** scaling (cheap to turn on later, as
long as nothing precludes it).

- **Stateless async API** — FastAPI async endpoints; no in-process state, sessions verified
  per-request → scale horizontally by adding instances behind a load balancer.
- **Background workers + queue** — all ingestion and CPU-bound analytics run in workers
  (Redis-backed, e.g. `arq`), never in the request path. The web tier stays thin and I/O-bound.
- **Storage tiering** — Postgres for relational data + derived aggregates; **object storage**
  for raw per-sample streams (compressed); Redis for caching computed analytics.
- **Deferred but not precluded** — read replicas, table partitioning, multi-region, autoscaling.
  We don't build these now; we make sure the design doesn't block them.

## Data sources & ingestion

Pluggable parsers feed **one canonical model** (`Activity` + `Sample[]`) →
analytics pipeline → storage. The analytics engine is **source-agnostic**: adding a new
data source means writing one parser that emits the canonical model — nothing downstream changes.

| Source | Module | Notes |
|--------|--------|-------|
| **Strava** | `ingest/strava_sync.py` | OAuth2 + activity streams. Webhook-driven (push). First to be built. |
| **NK CSV** | `ingest/csv_parser.py` | Direct upload. Full per-stroke fidelity. Co-equal path (see below). |
| **NK FIT** | `ingest/fit_parser.py` | Direct upload, via `fitdecode`. |

Strava streams (~1 Hz: time, GPS lat/lng, distance, speed, heart rate, cadence = stroke rate)
are sufficient for all core metrics. NK file upload adds exact per-stroke resolution.

Strava sync **filters to rowing activity types only** — don't import the user's runs/rides.

**Strava throughput is a hard ceiling at scale:** Strava's rate limit (200 req/15 min,
2,000/day) is **per-application, not per-user**, so polling does not scale to many athletes.
Webhook-driven (push) sync is the real Strava ingestion path, and **NK file upload is a
co-equal ingestion path** — the only one not bounded by Strava's app-wide limit. Build order
starts with Strava for the POC, but the architecture treats sources as equals.

**Validate early:** confirm Strava reports rowing `cadence` as true strokes-per-minute
(watch for any halving/doubling quirk carried over from cycling/running conventions).

## Auth

**Strava OAuth is the login.** Logging in = connecting Strava, which the user must do anyway
to grant data access. No separate passwords for now.

Identity is kept **decoupled** from Strava: a first-class `User` *has a* `StravaConnection`
(the OAuth tokens). Login = OAuth callback → find-or-create the `User` for that Strava
athlete. This leaves a clean seam to later add email/password (or magic-link) login and
CSV-only users — without welding identity to a Strava ID. Sessions signed with `SECRET_KEY`.

## Tech stack

- **Backend:** Python 3.12+, FastAPI + Uvicorn (async), Pydantic v2 (`pydantic-settings`).
  **Data access: psycopg 3 (async pool) + plain SQL** — async `aiosql`, `class_row` maps rows
  to Pydantic/dataclasses, `COPY` for bulk inserts. No ORM. Migrations: `yoyo-migrations`
  (plain SQL up/down). HTTP: async `httpx`. FIT: fitdecode. Strava via direct httpx (not stravalib).
  Analytics libraries: TBD — chosen once the metric implementations make requirements clear.
- **Background jobs:** Redis + `arq` worker for ingestion and analytics (off the request path).
- **Object storage:** S3-compatible (Railway bucket / R2 / S3) for raw streams.
- **Frontend:** React + TypeScript (Vite), TanStack Query, React Router, Plotly
  (`react-plotly.js`) or ECharts for zoomable time-series, Tailwind CSS.
- **Database:** PostgreSQL, accessed via plain SQL (no ORM). See data-access above.
- **Weather:** Open-Meteo (free, no API key), queried by activity start lat/lng + time.
  Note: the **archive** API lags real time by ~5 days, so recent activities won't be in it —
  use the Forecast API (`past_days`) or Historical-Forecast API for recent rows, archive for older.
- **Deploy:** Railway — stateless `api` + `web` + `worker` services, plus `postgres`, `redis`,
  and an object-storage bucket. Local dev via `docker-compose`.

## Repository layout

```
backend/
  app/
    main.py            # FastAPI app
    config.py          # settings (pydantic-settings)
    db.py              # psycopg async connection pool + query helpers
    storage.py         # object-storage client (raw streams)
    models/            # Pydantic/dataclass row + domain models
    schemas/           # Pydantic request/response models
    api/               # routers: auth, activities, ingest, analytics, strava_webhook
    ingest/            # strava_sync, csv_parser, fit_parser, normalize (dedupe)
    analytics/         # metrics, splits, weather
    worker/            # arq background tasks (ingestion, analytics)
    sql/               # .sql query files (loaded via aiosql)
  migrations/          # plain-SQL migrations (yoyo)
  pyproject.toml
frontend/              # Vite React + TS app
docker-compose.yml     # postgres + redis + api + worker + web for local dev
```

## Canonical data model

- **User** — an app user. Has zero or more `StravaConnection`s.
- **StravaConnection** — OAuth tokens + Strava athlete id for a `User`.
- **Activity** — one workout: owner (`User`), source, external id, start time, sport, totals,
  start lat/lng, name, pointer to its raw-stream object.
- **Sample** — a time-series point belonging to an Activity: `t` (seconds), `lat`, `lng`,
  `distance_m`, `speed_mps`, `stroke_rate_spm`, `heart_rate`, plus optional per-stroke extras.

**Storage tiering:** raw `Sample` streams are written as compressed objects (Parquet/JSON) to
**object storage**, keyed by activity. **Postgres** holds `User`, `StravaConnection`, `Activity`
metadata, and **derived aggregates/summaries** (what dashboards query). The primary DB never
holds billions of raw sample rows.

Dedupe activities across sources by start time / external id / content hash in
`ingest/normalize.py`.

## Intended analytics (definitions TBD)

The *outputs* we want; exact formulas, units, and edge-case handling (zero stroke rate during
rests, stopped/zero speed, GPS dropout/gaps) are decided when implementing `analytics/`.
**Getting data in comes first** — these are deferred on purpose.

- Split (pace per 500 m) and boat speed
- Stroke rate and distance-per-stroke
- Rate / speed / HR relationship curves and stroke efficiency
- Wind component (head / tail / cross) from GPS heading vs Open-Meteo wind direction
- Workout segmentation — pieces vs rest, with per-piece summaries
- Session summaries (totals + averages) and cross-session trends

Analytics run in the worker; results are cached (Redis) / persisted as derived aggregates, not recomputed per request.

## Commands

```bash
# Backend (from backend/)
uv run uvicorn app.main:app --reload     # dev API server
uv run arq app.worker.WorkerSettings     # background worker
uv run yoyo apply                        # apply migrations
uv run yoyo new -m "msg"                 # create a new migration

# Frontend (from frontend/)
npm run dev

# Full local stack
docker compose up
```

## Testing

- **Backend:** pytest (`asyncio_mode=auto`). Parsers/analytics are pure functions over the
  canonical model — test them directly with fixtures (sample Strava stream payloads, later NK
  CSV files). DB tests use the `db_conn` fixture (`tests/conftest.py`): an async connection
  whose work is rolled back per test, and which **skips** when no database is reachable (so
  `pytest` is green locally without infra; CI provides Postgres).
- **Frontend:** Vitest + React Testing Library.
- **CI:** `.github/workflows/ci.yml` runs backend tests (against a Postgres service, after
  `yoyo apply`) and a frontend build on every push/PR.

## Environment variables

`DATABASE_URL`, `REDIS_URL`, `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`,
`STRAVA_WEBHOOK_VERIFY_TOKEN`, `APP_BASE_URL`, `SECRET_KEY`,
`S3_ENDPOINT`, `S3_BUCKET`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`.
