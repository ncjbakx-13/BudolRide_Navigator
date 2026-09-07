# Engineering Standards

Status: working agreement for this repository. Adopt these rules as components are built; do not claim a rule is enforced until automation or code enforces it.

## Working rules

- Start each task by reading `AGENTS.md`, `docs/PROJECT.md`, `docs/DECISIONS.md`, and the relevant design document.
- Keep changes inside the v1 boundary. Record a deliberate scope change before building it.
- Prefer a small, working vertical slice over frameworks or abstractions that have no current user-facing use.
- Never copy production secrets into source code, examples, logs, issues, screenshots, or test fixtures.
- Preserve unit names and coordinate order at every boundary. API coordinates are longitude, latitude.

## Configuration and secrets

- Commit only `.env.example` files with non-working placeholders. Local `.env` files are ignored.
- Validate required settings once at application or job startup. Fail clearly when a required value is absent; do not use a hidden production fallback.
- Keep the Supabase service-role key server-side only. The mobile client may use only public configuration that is intended for a client build.
- Use separate local, test, and production database credentials with least privilege. Rotate credentials after exposure or team membership changes.

## Backend conventions

- Version real endpoints under `/api/v1`; keep the FastAPI demo endpoints separate from the application contract until removed.
- Define Pydantic models for every request and response. Use enums for POI categories and explicit minimum/maximum bounds for detour radius, coordinates, query limits, and pagination.
- Require a verified Supabase JWT before every route request. Do not introduce an anonymous route-preview exception without a confirmed decision change.
- Route handlers coordinate dependencies and return models. Services contain routing, selection, and elevation logic. Repositories own database access.
- Authorize before database reads or writes involving a user. Return `401` for missing or invalid credentials and `403` for authenticated but unauthorized access.
- Use a global error handler with stable error codes. Log a request ID and sanitized context; never return SQL, tokens, connection strings, or stack traces to clients.
- Set database statement timeouts and HTTP client connect/read timeouts. Bound retries and retry only failures that are safe to retry.

## Frontend conventions

- Use TypeScript with strict compiler settings. Treat API response models as a contract, not loosely typed JSON.
- Keep route form state, network state, and map rendering separate so a temporary provider failure does not corrupt user input.
- Store tokens only in platform secure storage after the authentication decision is confirmed. Do not use a JavaScript-accessible persistent store for credentials.
- Validate obvious input locally for responsiveness, then rely on server validation as the authority.
- Give loading, empty, timeout, offline, and permission-denied states explicit UI treatment. Location permission is optional and must have a manual-origin fallback.

## Database and migration conventions

- Make schema changes through Alembic once the backend database layer is introduced. ETL-only bootstrap SQL must remain idempotent and documented until migrated.
- Use `geometry(..., 4326)` for stored source geometry and GiST indexes for spatial searches. Use `geography` casts or a projected CRS for meters; do not compare degrees as distance.
- Design external identifiers as `(source, source_element_type, source_id)`. OSM node, way, and relation numeric IDs are not globally unique across element types.
- Use explicit transaction boundaries. A failed ETL run must not leave a half-applied dataset marked current.
- Add an index only for an observed query pattern; use `EXPLAIN (ANALYZE, BUFFERS)` against representative data before calling a spatial query optimized.

## Tests and quality gates

| Area | Minimum check before merge |
| --- | --- |
| Frontend | TypeScript check, Expo lint, and a device or emulator smoke test for changed user flows |
| Backend | Unit tests for services, API tests for validation/auth/error paths, and a database integration test for spatial queries |
| ETL | Fixture-based parsing test, idempotent rerun test, malformed-source test, and a transaction rollback test |
| Routing profile | Known-route regression cases for prohibited roads, bike-friendly roads, and a route with no eligible POI |
| Security-sensitive change | Threat review of data access, auth boundary, logging, and secret handling |

Add CI checks only after the local command is stable and documented. CI should fail on formatting, lint, tests, dependency audit findings that are actionable, and leaked secrets.

## Observability and performance

- Emit structured logs with timestamp, level, request or job ID, duration, dependency outcome, and sanitized error code.
- Collect route latency, OSRM error rate, ETL duration, records fetched/accepted/rejected, POI freshness, database query time, and cache effectiveness before tuning.
- Paginate lists, cap spatial candidates, select only required columns, and precompute or cache expensive profiles where measurement justifies it.
- Add a timeout budget for the complete route request. Degrade gracefully when optional elevation enrichment is unavailable instead of retrying indefinitely.

## Definition of done

A change is done when its behavior, validation, error state, tests, documentation, and configuration requirements are clear. Update the relevant decision or design document when the change modifies a contract, schema, security boundary, or operational runbook.
