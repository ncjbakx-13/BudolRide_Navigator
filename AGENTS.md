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

- **Aaron Angat** — Full-Stack Engineer (Backend API & Mobile UI: Node.js, React Native)
- **NCJ Bakx (Nathaniel)** — Data Engineer (Data Infrastructure & Routing Engine: Python, PostGIS, OSRM)

## Tech Stack
- **Mobile app:** React Native with Expo, TypeScript
- **Map rendering:** react-native-maps
- **Backend API:** Node.js + Express
- **Database:** PostgreSQL + PostGIS (hosted on Supabase)
- **Auth:** Supabase Auth
- **Routing engine:** OSRM (Docker, local for dev; Render for later hosting)
- **Data ingestion / ETL scripts:** Python (separate from the main app — used only
  for one-off scripts pulling from Overpass API / OpenTopoData / Wikidata)
- **Backend hosting:** Render (free tier)
- **Mobile build/distribution:** Expo EAS Build

## Repo Structure
- `frontend/` — React Native (Expo) app — owned by Aaron
- `backend/` — Node.js + Express API — owned by Aaron
- `data-engineering/` — Python ETL scripts, PostGIS setup, OSRM config — owned by Nathaniel
- `docs/` — full project proposal & planning docs

## Conventions
- Use TypeScript for all React Native and Node.js code (loose typing is fine while learning).
- Keep Python isolated to `data-engineering/` — not part of the app runtime.
- Cache OSM/Overpass API results in PostGIS rather than querying live on every request
  (Overpass has rate limits).
- Detour Radius input range: 0.5 km–5 km.

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
- Backend: `npm run dev` (from `backend/`)
- Routing engine: `docker compose up` (from `data-engineering/`)

## Reference
Full proposal, feature descriptions, and data source links: `docs/PROJECT.md`