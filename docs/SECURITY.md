# Security Baseline

Status: required design standard. The repository is still being scaffolded, so this document distinguishes required controls from controls already implemented.

## Immediate remediation

A plaintext database credential was found in the initial ETL source and has been removed from the working tree. Treat it as exposed even if the repository is private.

1. Rotate the affected database password or connection string in the database provider.
2. Replace all deployments and developer `.env` files with the new value.
3. Verify the committed Git history, pull requests, screenshots, and logs do not still expose it. History rewriting is a separate team decision; rotation is mandatory regardless.
4. Do not commit the replacement. Use `data-engineering/.env` locally and the hosting platform's secret store in deployed environments.

## Assets and trust boundaries

| Asset | Boundary | Required protection |
| --- | --- | --- |
| Supabase service-role key and database credentials | Server and ETL only | Secret store, least privilege, rotation, no client delivery |
| Supabase user access token | Mobile to API | TLS, secure device storage, issuer/audience/signature/expiry validation |
| Saved routes and preferences | Authenticated user data | Ownership checks on every read/write and minimal retention |
| Public POI and road data | ETL to database | Source provenance, validation, rate limits, and attribution |
| OSRM and database services | Internal infrastructure | Not publicly writable; network and credential restrictions |

## Required controls before the first route endpoint ships

### Authentication and authorization

- FastAPI validates Supabase JWT signature using current trusted keys and validates issuer, audience, expiry, and required claims. Do not decode a token without verification.
- Require authentication by default for user-owned resources. Attach the authenticated subject to queries and enforce ownership in SQL or repository methods.
- Keep a distinct application database role for FastAPI and a separate ETL role. Neither role is a mobile-client credential.
- If Supabase client-side database access is ever introduced, enable and test Row Level Security for every exposed table. The current intended architecture keeps application data access behind FastAPI.

### API and network protection

- Serve production API traffic over HTTPS only. Configure exact production CORS origins; do not use `*` with credentials.
- Enforce maximum request body size, coordinate ranges, enum values, pagination limits, and a detour radius of 0.5 km to 5 km.
- Apply rate limits by authenticated user where available and by IP for anonymous endpoints. Apply tighter limits to route calculations and authentication-adjacent endpoints.
- Set upstream timeouts, bounded retry budgets, and circuit-breaking or fast-fail behavior for OSRM and public data dependencies.
- Return generic client errors. Keep dependency details and tracebacks only in protected logs.

### Data and secrets

- Use parameterized SQL and allowlisted sort/filter fields. Never interpolate coordinate, route, or user input into SQL or shell commands.
- Put secrets only in environment variables or a deployment secret manager. `.env.example` contains placeholders only.
- Minimize location data. Do not persist precise origins, destinations, or route history unless a confirmed user feature needs it. Define retention before storage is added.
- Redact `Authorization` headers, cookies, database URLs, coordinates associated with users, and provider payloads from routine logs.

### Mobile security and privacy

- Request location permission only when the user chooses a location-based action, explain the purpose in app text, and preserve manual coordinate/search entry.
- Store access tokens in platform secure storage, not AsyncStorage or source-controlled config.
- Do not put privileged keys in `app.json`, public Expo config, source maps, or a bundle. Assume every client-bundled value is public.
- Display data-source attribution and a route-safety disclaimer before release; a bicycle-friendly route is not a guarantee of current road safety.

## Verification checklist

- A missing, expired, malformed, wrong-issuer, or wrong-audience token is rejected.
- User A cannot read or modify User B's saved resource.
- Invalid coordinates, oversized payloads, unknown fields, and out-of-range detour values fail validation without a dependency call.
- API responses and logs do not include secrets, raw SQL, provider credentials, or stack traces.
- ETL cannot start without a configured database URL and succeeds only over its configured endpoint.
- Dependency and secret scanning are included in the future CI pipeline.

## Incident handling

When a secret, personal location record, or unauthorized access is suspected: stop sharing the value, revoke or rotate the credential, preserve minimal evidence, assess affected data, remediate the code/configuration path, and record the event in a private team channel. Do not paste sensitive values into tickets or commits.
