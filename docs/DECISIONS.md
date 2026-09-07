# Decisions and Open Questions

Use this file to prevent plans from becoming accidental facts. A statement is binding only when it is marked **Confirmed**. Proposed controls describe intended work, not implemented behavior.

## Confirmed baseline

| Topic | Decision | Source |
| --- | --- | --- |
| Product scope | Online, POI-aware bicycle route planning for Cavite only | `README.md`, `docs/PROJECT.md` |
| Mobile | React Native, Expo, TypeScript, Expo Router | `AGENTS.md`, `frontend/package.json` |
| API | FastAPI with Pydantic and OpenAPI | `AGENTS.md` |
| Spatial database | PostgreSQL with PostGIS on Supabase | `AGENTS.md` |
| ORM and migrations | SQLAlchemy, GeoAlchemy2, Alembic | `AGENTS.md` |
| Authentication provider | Supabase Auth; FastAPI validates protected-route JWTs | `AGENTS.md` |
| Routing | OSRM in Docker locally; later hosting is undecided in capacity terms | `AGENTS.md` |
| Public-source caching | Cache source data in PostGIS, not per-user live Overpass requests | `AGENTS.md` |
| Detour bounds | 0.5 km to 5 km | `AGENTS.md` |
| Route access | A user must sign in before making any route request | User decision, 2026-09-07 |
| Python baseline | Python 3.12 is the minimum supported runtime | User decision, 2026-09-07 |
| V1 exclusions | Offline mode, live traffic, UGC, social features, push notifications, and NCR coverage | `AGENTS.md` |

## Open decisions

| ID | Question | Why it must be decided | Suggested owner |
| --- | --- | --- | --- |
| D-002 | Which map provider and platform credentials will be used for Android, iOS, and web? | `react-native-maps` configuration and key handling differ by platform | Aaron |
| D-004 | What measurable bicycle-safety policy will the OSRM profile apply? | "Safe" needs testable road-class exclusions and weights, not a vague claim | Nathaniel |
| D-005 | How often are OSM POIs and elevation data refreshed, and how is stale data shown or handled? | Affects ETL cost, provenance, and user trust | Nathaniel |
| D-006 | Can the intended OSRM deployment fit the chosen hosting memory and disk limits? | Regional routing graphs can exceed free-tier capacity | Nathaniel |
| D-007 | What source attribution and license notices are required in the mobile UI and documentation? | OSM and other source terms must be honored before release | Aaron and Nathaniel |

## Confirmed decision records

### D-001: Require sign-in before route requests

- Status: Confirmed
- Date: 2026-09-07
- Owner: Aaron
- Decision: All route-preview and future route endpoints require a signed-in Supabase user. There is no anonymous route preview in v1.
- Consequences: FastAPI JWT validation, a signed-out mobile state, and authenticated rate-limit behavior are prerequisites for the first route endpoint.

### D-003: Support Python 3.12

- Status: Confirmed
- Date: 2026-09-07
- Owner: Aaron
- Decision: Python 3.12 is the minimum supported runtime for backend and supporting Python tooling.
- Consequences: During the implementation phase, update `backend/pyproject.toml`, lockfiles, CI, and setup documentation to remove the current 3.14-only requirement. Use dependencies and syntax compatible with Python 3.12.

## Decision record template

Add a new record when an open decision is resolved or an important tradeoff is made.

```md
### D-008: Short title

- Status: Proposed | Confirmed | Superseded
- Date: YYYY-MM-DD
- Owner: Name
- Context: What prompted this decision?
- Decision: What will the project do?
- Consequences: What becomes easier, harder, or deferred?
- Evidence: Link to benchmark, issue, source, or test result.
```

Do not silently convert a proposed approach into a confirmed decision. When a decision is superseded, retain the old record and link to its replacement.
