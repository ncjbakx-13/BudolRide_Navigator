# Architecture Baseline

Status: design baseline. This document describes the intended v1 architecture. It does not mean every control or component is implemented. See `docs/DECISIONS.md` before treating an undecided item as a requirement.

## Product boundary

BudolRide Navigator is an online, POI-aware bicycle route-planning app for Cavite, Philippines. A rider previews a safer bicycle-oriented route, may request an optional detour through eligible POIs, and sees elevation and steep-climb information before starting the ride.

V1 excludes offline routing, live traffic, user-generated content, social features, push notifications, and coverage outside Cavite.

## Current repository state

| Area | Current state | Do not assume |
| --- | --- | --- |
| `frontend/` | Expo Router starter application | Maps, authentication, or route screens exist |
| `backend/` | FastAPI starter with demo in-memory account endpoints | Database, authorization, or route APIs exist |
| `data-engineering/` | Initial PostGIS POI schema and an OSM bicycle-shop loader | Repeatable ETL, provenance, or production data are complete |

The demo account endpoint is learning code, not an API contract. Replace it with versioned, validated application endpoints instead of extending it into production behavior.

## Target component boundaries

```text
Expo mobile app
        |
        v
FastAPI API -----> OSRM bicycle profile
        |
        +---------> PostgreSQL + PostGIS <--------- ETL jobs
                              ^                       |
                              |                       +-- OSM/Overpass
                              |                       +-- OpenTopoData
                              |                       +-- Wikidata (optional)
                              |
                        cached, attributed data
```

### Mobile application

- Collect route preferences and show only API-ready, validated values.
- Render route geometry, selected POIs, and elevation data returned by the API.
- Keep access tokens in platform secure storage when authentication is introduced; never bundle database credentials, Supabase service-role keys, or routing-provider secrets.
- Treat map and route data as a preview, not turn-by-turn safety advice.

### FastAPI application

- Own the public API contract, authentication boundary, request validation, authorization, response shaping, and rate limits.
- Keep route handlers thin. Put POI selection, elevation analysis, and routing orchestration in services.
- Use parameterized SQL through SQLAlchemy/GeoAlchemy2. PostGIS performs spatial filtering and distance calculations.
- Make external calls time-bounded and failure-tolerant. A route request must return a clear dependency error rather than hang indefinitely.

### PostGIS database

- Store canonical cached POIs, spatial metadata, ETL run records, and later user-owned preferences or saved routes.
- Store source geometry in `geometry(..., 4326)`. Cast to `geography` or transform to a suitable projected CRS for meter-based calculations.
- Restrict direct database access to API and ETL service roles. The mobile app does not connect to PostgreSQL.

### Routing engine

- OSRM produces base and waypoint routes from prepared regional road data.
- The OSRM bicycle profile must explicitly prohibit expressways and model bicycle suitability. Its exact weights are an open decision and must be tested against known Cavite routes.
- OSRM is not the source of truth for POIs, user data, or authentication.

### ETL jobs

- Fetch public source data on a schedule or controlled manual run, normalize it, validate it, then upsert it into PostGIS in a transaction.
- Record source, source identifier, source element type, retrieval time, source URL/query version, and freshness state. Preserve enough provenance to reproduce a result.
- Never query Overpass or elevation providers synchronously for every user route request.

## Route-planning flow

1. A signed-in mobile app sends validated start, end, preferences, and a detour radius between 0.5 km and 5 km. FastAPI verifies the Supabase JWT before any route dependency call.
2. FastAPI asks OSRM for a base bicycle route and rejects routes outside the Cavite v1 coverage boundary.
3. FastAPI queries cached POIs near the route with indexed PostGIS predicates such as `ST_DWithin`.
4. A service scores candidates using declared, testable criteria: requested category, route proximity, data freshness, and route-cost impact. Safety is enforced by the routing profile, not guessed from POI popularity.
5. FastAPI asks OSRM to route through zero or one selected waypoint for the first vertical slice. Multi-stop optimization is deferred until scoring and correctness are measured.
6. The service calculates or retrieves an elevation profile, identifies segments over the documented steepness threshold, and returns route geometry plus transparent summary metadata.

## API contract principles

- Version public endpoints under `/api/v1` once real endpoints are introduced.
- Use typed Pydantic request and response models. Reject unknown request fields for public writes and reject invalid coordinate ranges, categories, and pagination values.
- Return GeoJSON-compatible geometry and explicit units. Coordinate order is longitude, latitude; distances are meters in API payloads unless a field name states otherwise.
- Publish only data needed by the mobile feature. Apply a hard response size and candidate limit to every spatial query.
- Document errors with stable machine-readable codes, not raw dependency exceptions.

## First vertical slice

The smallest useful end-to-end feature is an authenticated Cavite route preview with no optional POI detour: validated coordinates, an OSRM route, route geometry on the map, total distance/duration, and a clearly incomplete elevation state. Add cached POI detours only after the base route, API contract, and PostGIS index behavior are verified.

## Architecture changes

Record changes that affect a public contract, data model, infrastructure choice, security boundary, or routing policy in `docs/DECISIONS.md`. Update this document only after the decision is made.
