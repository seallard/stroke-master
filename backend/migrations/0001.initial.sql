-- Initial schema: users, strava_connections, activities.
-- Raw sample streams live in object storage (activities.stream_object_key);
-- derived aggregates live in activities.summary (jsonb).

create table users (
    id uuid primary key default gen_random_uuid(),
    email text unique,
    created_at timestamptz not null default now()
);

create table strava_connections (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users (id) on delete cascade,
    athlete_id bigint not null unique,
    access_token text not null,
    refresh_token text not null,
    expires_at timestamptz not null,
    scope text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table activities (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references users (id) on delete cascade,
    source text not null,
    external_id text,
    sport text,
    name text,
    start_time timestamptz not null,
    elapsed_time_s integer,
    distance_m double precision,
    start_lat double precision,
    start_lng double precision,
    stream_object_key text,
    summary jsonb,
    weather jsonb,
    created_at timestamptz not null default now(),
    unique (user_id, source, external_id)
);

create index activities_user_start_idx on activities (user_id, start_time desc);
