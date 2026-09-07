---
name: budolride-navigator-engineering
description: Apply BudolRide Navigator's product, architecture, security, and spatial-data guardrails when planning, implementing, reviewing, or operating this repository.
---

# Budolride Navigator Engineering

Use this skill for work in the BudolRide Navigator repository. It turns the repository's deliberate decisions into implementation constraints without treating proposed work as completed.

## Establish facts first

Read `AGENTS.md`, `docs/PROJECT.md`, and `docs/DECISIONS.md` before changing behavior. Read the relevant design document before working in its area:

- `docs/ARCHITECTURE.md` for service boundaries, routing flow, and API shape.
- `docs/SECURITY.md` for credentials, authentication, authorization, privacy, logging, and deployment configuration.
- `docs/DATA_OPERATIONS.md` for ETL, PostGIS schemas, source provenance, and spatial queries.
- `docs/ENGINEERING_STANDARDS.md` for validation, tests, performance, and completion checks.
- `docs/DELIVERY_PLAN.md` for sequencing a feature from the current scaffold.

Treat only **Confirmed** entries in `docs/DECISIONS.md` as project decisions. Name an assumption, record a new decision, or ask a focused question when an unresolved choice would materially change the implementation. Never report a documented target control as implemented without code and verification.

## Preserve the v1 boundary

Keep work focused on online, Cavite-only bicycle route planning, cached POIs, optional detours between 0.5 km and 5 km, and pre-ride elevation awareness. Do not add offline maps, real-time traffic, user-generated content, social features, push notifications, or NCR coverage unless the user explicitly changes scope.

Route requests require a signed-in user; do not introduce anonymous route preview. Use Python 3.12-compatible dependencies and syntax. The existing backend runtime configuration must be reconciled when code changes are authorized.

## Build through explicit boundaries

- Use TypeScript for the Expo application and Python for API and ETL work.
- Make FastAPI endpoints typed, versioned, and thin; put routing, POI selection, and elevation behavior in services.
- Use parameterized SQL or SQLAlchemy/GeoAlchemy2. Let PostGIS execute spatial filtering and meter-based distance work.
- Keep the mobile client behind the FastAPI public API. Do not deliver database credentials or Supabase service-role privileges to it.
- Cache public data in PostGIS. Do not put Overpass, Wikidata, or elevation calls on an unbounded user-request path.
- Start new routing behavior with a base route, then a bounded single-POI detour. Add multi-stop optimization only when measured requirements justify it.

## Apply security and data safeguards

- Treat every credential found in source, output, or history as exposed: do not repeat it, remove it from the working copy, and instruct the team to rotate it.
- Validate Supabase JWT signature, issuer, audience, expiry, and user ownership before protected operations. Do not treat token decoding as validation.
- Bound coordinates, payloads, candidate counts, pagination, route timeouts, and external retries.
- Store source geometry as SRID 4326 and use `geography` or a tested projected CRS for meter calculations. Maintain external POI identity with source, element type, and source ID.
- Record source provenance and ETL freshness. A failed refresh must not mark partial data current.

## Verify proportionally

Run the smallest meaningful checks for the changed layer, then verify the user-facing or operational outcome. For security-sensitive work, test both the allowed path and the rejected path. For spatial and routing work, use known Cavite fixtures and state what data/profile conditions were tested.

Update the matching documentation when a public contract, schema, security boundary, operational process, or confirmed decision changes.
