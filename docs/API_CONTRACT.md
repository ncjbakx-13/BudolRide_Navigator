# API Contract Baseline

Status: proposed contract. This is the design target for the first real FastAPI endpoints, not a statement that these endpoints exist. Implement it with Pydantic models and API tests before treating it as stable.

## Global rules

- All route endpoints require a valid Supabase access token. There is no anonymous route preview in v1.
- Use `/api/v1` for application endpoints. Use JSON request and response bodies, except documented health probes.
- Coordinates are WGS84 longitude followed by latitude. Distances are meters and durations are seconds unless the field name says otherwise.
- Reject unknown public request fields, invalid coordinate ranges, unsupported categories, oversized payloads, and detour radii outside 500 m to 5,000 m before calling OSRM or PostGIS.
- Return only the minimum route and POI data needed for the screen. Never return internal provider URLs, database identifiers, or raw dependency errors.

## Authentication

Every protected request includes:

```http
Authorization: Bearer <Supabase access token>
```

FastAPI must verify the token signature, issuer, audience, expiry, and subject. An absent or invalid token returns `401`. A valid token without permission for a user-owned resource returns `403`.

## Proposed route preview

`POST /api/v1/routes/preview`

```json
{
  "origin": { "longitude": 120.9, "latitude": 14.3 },
  "destination": { "longitude": 120.8, "latitude": 14.4 },
  "preferences": {
    "poi_categories": ["cafe", "bicycle_repair"],
    "detour_radius_m": 2000,
    "include_elevation": true
  }
}
```

The request shape above illustrates field names and units. The final coordinate and category models must be generated from shared TypeScript/Pydantic contract decisions, not copied as untyped JSON.

The response should include:

- A GeoJSON `LineString` route geometry.
- Total distance and estimated duration.
- The routing profile and data freshness metadata needed to explain the result.
- At most one selected POI for the first detour implementation, including category, display name, coordinates, source attribution, and a selection reason.
- An elevation summary and samples when available, or an explicit `unavailable` state when optional elevation enrichment fails.
- A request ID for support and log correlation.

Do not promise live conditions, turn-by-turn navigation, or guaranteed road safety in the API response.

## Proposed errors

Use a consistent body with a stable code and a user-safe message:

```json
{
  "error": {
    "code": "route_outside_coverage",
    "message": "Both route points must be within the Cavite coverage area.",
    "request_id": "opaque-request-id"
  }
}
```

Initial error codes:

| HTTP status | Code | Meaning |
| --- | --- | --- |
| 401 | `authentication_required` | Token missing, invalid, expired, or rejected |
| 403 | `forbidden` | Authenticated user lacks ownership or permission |
| 422 | `validation_error` | Input does not meet documented constraints |
| 429 | `rate_limited` | Caller exceeded route or API limits |
| 502 | `routing_unavailable` | OSRM or an upstream routing dependency failed |
| 503 | `elevation_unavailable` | Required elevation dependency is unavailable and no valid fallback exists |
| 503 | `data_refresh_in_progress` | Route data is intentionally unavailable during an unsafe publish state |

Choose whether missing optional elevation should return a successful partial route or `503` before implementation. Record the decision in `docs/DECISIONS.md`.

## Endpoint sequencing

1. `GET /health/live` and `GET /health/ready` for process and dependency checks.
2. Authenticated `POST /api/v1/routes/preview` with a base OSRM route only.
3. Bounded cached-POI selection and one optional waypoint.
4. Elevation profile enrichment with an explicit partial-result policy.
5. User-owned saved routes and preferences after authorization tests exist.

Do not add write endpoints for accounts. Supabase Auth is the identity authority; application data starts only when a confirmed feature requires it.
