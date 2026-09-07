# Test Strategy

Status: test plan for the first implementation phase. Tests should verify observable product and safety behavior, not merely internal implementation details.

## Principles

- No test depends on live Overpass, OpenTopoData, Wikidata, Supabase, or a public OSRM instance. Use fixtures, fakes, or a controlled local service.
- Use small, named Cavite fixtures for roads, POIs, elevation samples, and expected routes. Keep their origin and license status documented.
- Test rejection paths as deliberately as success paths. Security, validation, and data-quality failures are product behavior.
- Prefer deterministic inputs. Persist a failing spatial or routing case as a regression fixture before changing an algorithm or profile.

## Backend tests

| Layer | Required coverage |
| --- | --- |
| Settings | Missing or malformed required settings fail at startup without exposing secrets |
| Authentication | Missing, expired, invalid-signature, wrong-issuer, wrong-audience, and valid Supabase JWT paths |
| Validation | Coordinate bounds, Cavite coverage, known POI categories, 500 m to 5,000 m detour range, body-size and candidate limits |
| Services | Base route, no eligible POI, one eligible POI, failed optional elevation, and bounded dependency retry behavior |
| Database | Indexed corridor query, source-element identity, pagination, transaction rollback, and user ownership when user data is introduced |
| API contract | Response schema, error-code stability, `401`/`403` distinction, and no internal error leakage |

## ETL tests

- Parse valid node and way source fixtures without conflating their external identities.
- Reject records with invalid/missing coordinates, unknown source type, malformed payload, or unsupported geometry.
- Verify identical input can rerun without duplicate records.
- Verify a failed insert rolls back the whole publish transaction and leaves the prior canonical dataset current.
- Verify request timeout and retry behavior with a fake provider; do not sleep in unit tests.
- Assert run metrics account for fetched, accepted, rejected, inserted, updated, and retired records.

## Routing-profile regression tests

Maintain a small suite of start/end pairs representing Cavite conditions. Each case records whether a road class must be prohibited, avoided, preferred, or merely allowed. Review route geometry after OSRM profile changes; duration alone is not enough to detect an unsafe regression.

## Frontend tests

- Type-check API models and route state.
- Test signed-out redirect and signed-in route submission behavior.
- Test route form validation, loading, success, empty candidate, timeout, elevation-unavailable, and authorization-expired states.
- Run a physical-device or emulator smoke test for map rendering, manual origin/destination input, and location-permission denial.
- Do not depend on platform map pixels for unit tests. Use an integration or manual smoke test for native map behavior.

## Quality gates

Before a feature merges, run the relevant type check/lint, unit tests, integration tests for changed API or database behavior, and a manual smoke test for changed mobile flows. Before release, run dependency scanning, secret scanning, route-profile regressions, authenticated authorization tests, and a mobile permission/privacy review.

Record the exact commands in a future local-development guide only after they work from a clean clone on the selected Python 3.12 baseline.
