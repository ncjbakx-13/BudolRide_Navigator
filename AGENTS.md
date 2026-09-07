# AGENTS.md — BudolRide Navigator

> Read `docs/PROJECT.md` for full project background, problem statement, and data source links. This file is the quick-reference AI agents should follow every session.

## What this project is
A POI-aware bicycle navigation & topographic routing app for Cavite, Philippines.
Instead of fastest-route-for-cars, it routes cyclists onto safe bike lanes/backroads,
optionally detours through cafes/repair shops/scenic stops, and shows elevation
climbs before the ride starts.

## Team context
Two-person team, first-time project, no fixed deadline. Prefer simple,
well-documented, beginner-friendly approaches over clever/advanced ones.
Explain non-obvious steps rather than assuming prior experience.

- **Aaron Angat** — Full-Stack Engineer (Backend API & Mobile UI: FastAPI, React Native)
- **NCJ Bakx (Nathaniel)** — Data Engineer (Data Infrastructure & Routing Engine: Python, PostGIS, OSRM)

## Tech Stack
- **Mobile app:** React Native with Expo, TypeScript
- **Map rendering:** react-native-maps
- **Backend API:** Python + FastAPI
- **API validation and documentation:** Pydantic + FastAPI OpenAPI/Swagger
- **Database:** PostgreSQL + PostGIS (hosted on Supabase)
- **Database access and migrations:** SQLAlchemy + GeoAlchemy2, Alembic
- **Auth:** Supabase Auth
- **Routing engine:** OSRM (Docker, local for dev; Render for later hosting)
- **Data ingestion / ETL scripts:** Python (pulling from Overpass API / OpenTopoData /
  Wikidata)
- **Backend hosting:** Render (free tier)
- **Mobile build/distribution:** Expo EAS Build

## Repo Structure
- `frontend/` — React Native (Expo) app — owned by Aaron
- `backend/` — FastAPI application and API tests — owned by Aaron
- `data-engineering/` — Python ETL scripts, PostGIS setup, OSRM config — owned by Nathaniel
- `docs/` — full project proposal & planning docs

## Conventions
- Use TypeScript for React Native code and Python for backend and data-engineering code.
- Use Pydantic request/response models for FastAPI endpoints; keep route handlers thin
  and place routing or POI-selection logic in service modules.
- Use SQLAlchemy/GeoAlchemy2 or parameterized SQL. Let PostGIS perform spatial filtering
  and distance calculations where practical.
- Validate Supabase JWTs on protected FastAPI endpoints; never expose service-role keys
  to the mobile client.
- Cache OSM/Overpass API results in PostGIS rather than querying live on every request
  (Overpass has rate limits).
- Detour Radius input range: 0.5 km–5 km.

## Engineering source of truth
- Read `docs/DECISIONS.md` before relying on a design choice. Only entries marked
  **Confirmed** are binding; a proposal is not an implemented feature.
- Read `docs/ARCHITECTURE.md` before changing service boundaries or API/data flow,
  `docs/SECURITY.md` before changing auth, secrets, or data access, and
  `docs/DATA_OPERATIONS.md` before changing ETL or spatial schemas.
- Apply the repository-local `budolride-navigator-engineering` skill at
  `.codex/skills/budolride-navigator-engineering/SKILL.md` for BudolRide planning,
  implementation, review, and operations work.
- Do not claim authentication, routing safety, data freshness, database migrations,
  or any security control is implemented without verified code and tests.
- Route preview requires an authenticated user. Do not add anonymous route endpoints
  unless `docs/DECISIONS.md` is explicitly changed.
- Python 3.12 is the minimum supported runtime. The current backend configuration
  still requires Python 3.14 and must be reconciled when implementation work begins.
- If a credential is found in source, logs, fixtures, or documentation: stop using
  it, remove it from the working copy, and flag rotation. Never repeat it in output.

## Out of Scope for v1 (do not build these unless explicitly asked)
- Offline routing / offline maps
- User-generated content (reviews, ratings, POI submissions)
- Live traffic / real-time road conditions
- Multi-user or social features (shared rides, friends, leaderboards)
- Push notifications
- Coverage outside Cavite province (NCR expansion is future work)

## Build & Run
> Fill in further detail once each part is scaffolded, e.g.:
- Frontend: `npx expo start` (from `frontend/`)
- Backend: `uvicorn app.main:app --reload` (from `backend/`, after activating `.venv`)
- Routing engine: `docker compose up` (from `data-engineering/`)

## Reference
Full proposal, feature descriptions, and data source links: `docs/PROJECT.md`
