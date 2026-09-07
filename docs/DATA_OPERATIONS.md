# Data Operations

Status: target operating model for OSM, elevation, and optional Wikidata ingestion. Implement the items progressively, starting with a reproducible POI refresh.

## Source register

| Source | Intended use | Handling rule |
| --- | --- | --- |
| OpenStreetMap through Overpass | Roads, bike lanes, POIs, viewpoints, and repair-related locations | Fetch in controlled ETL runs, cache in PostGIS, preserve source IDs and attribution metadata |
| OpenTopoData | Elevation samples and route profiles | Batch or cache results; never call once per map render or unbounded user interaction |
| Wikidata Query Service | Optional enrichment for tourist destinations | Treat as secondary metadata; retain source and refresh metadata separately from canonical POIs |

Before release, confirm and display all required source attribution and license notices. Source terms may change, so use the linked primary documentation from `docs/PROJECT.md` when implementing the release UI.

## Canonical POI requirements

Each canonical POI should eventually have at least:

| Field | Purpose |
| --- | --- |
| `source` | Identifies OSM, Wikidata, or another provider |
| `source_element_type` and `source_id` | Creates a stable external key; OSM node, way, and relation IDs can overlap |
| `name` and normalized category | Supports display and requested-stop filtering |
| `geom` | PostGIS point or representative point in SRID 4326 |
| `tags` or selected raw attributes | Preserves useful source context without inventing values |
| `retrieved_at`, `source_updated_at` when available, and `run_id` | Supports freshness and reproducibility |
| `is_active` or equivalent | Allows a refresh to retire missing source records safely |

The initial `spatial_pois` table uses a unique `osm_id` while its query collects both OSM nodes and ways. Do not rely on that key for a complete long-term dataset; replace it with an element-type-aware identity in a deliberate migration before broad ingestion begins.

## Geospatial rules

- Source coordinates are stored as `geometry` with SRID 4326. Longitude comes before latitude in GeoJSON, PostGIS point construction, and API payloads.
- Build a GiST index on geometry. Use `ST_DWithin(geom::geography, route_geom::geography, meters)` for meter-based route corridors unless a tested projected CRS is selected.
- Filter with a bounding box or indexed spatial predicate before expensive distance, line, or ranking calculations.
- Validate coordinates are finite and within longitude `-180..180`, latitude `-90..90`, then reject geometry outside the Cavite v1 coverage policy.
- Return only a bounded number of candidates. A wide detour radius must not turn into an unbounded table scan.

## ETL workflow

1. Create an ETL run record with source, query/profile version, start time, and status `running`.
2. Request source data over HTTPS using a distinct User-Agent, explicit connect/read timeout, bounded exponential backoff, and source-respecting rate limits.
3. Validate schema, source IDs, element type, coordinates, category mapping, and duplicate keys before loading.
4. Stage valid records, then upsert canonical records inside one transaction. Mark the run successful only after the transaction commits.
5. Record fetched, accepted, rejected, inserted, updated, and retired counts. Keep a reason for rejected records.
6. Generate a small data-quality report and investigate a material count or geographic-distribution change before publishing the refresh.

ETL jobs must be safe to rerun. A repeated run with identical source data should produce no duplicate POIs and should not erase a previously good dataset after a partial provider failure.

## Performance and quality practices

- Prefer batch inserts/upserts over one commit per POI. Use a staging table or batched parameterized statements once datasets grow.
- Cache raw provider responses or query snapshots only when storage and source terms allow it; otherwise retain query text, version, checksum, and summary metrics.
- Separate raw ingestion, normalization, and publish steps so a parsing change can be replayed without re-querying a rate-limited source.
- Analyze and vacuum tables after material refreshes when appropriate for the hosting plan.
- Measure representative spatial queries with `EXPLAIN (ANALYZE, BUFFERS)`. Add indexes only where observed plans justify them.
- Treat unnamed POIs and uncertain categories as valid data-quality states, not fields to fabricate. Display fallbacks clearly in the app.

## Elevation-specific guidance

- Sample a route at a controlled spacing and cap the number of elevation requests per route.
- Store profile source, sample spacing, units, generation time, and the route geometry or route hash used to create it.
- Calculate gradient from distance and elevation change with documented smoothing. The `> 8%` steep-climb threshold is a product rule; expose it as a clearly named summary, not a claim that every climb is detected exactly.
- Return the base route if optional elevation enrichment fails, with an explicit unavailable state.

## Operational checks

- Run a small Cavite fixture before a full source refresh.
- Monitor provider failures, retries, duration, row counts, reject reasons, stale-data age, and database transaction failures.
- Keep production ETL credentials in the deployment secret store and use a separate least-privilege role from the API service.
- Do not run destructive refreshes against the canonical table without a restorable snapshot and a reviewed migration or runbook.
