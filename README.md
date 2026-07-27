# 🚴 BudolRide Navigator

A POI-aware bicycle navigation & topographic routing app for cyclists in Cavite, Philippines.

Unlike typical car-first navigation apps, BudolRide Navigator routes cyclists onto **safe bike lanes and backroads**, optionally detours through cafes, repair shops, or scenic stops, and shows **elevation climbs** before the ride even starts.

> 📌 A 2-person team project built to learn React Native, Node.js, and geospatial data engineering.

---

## The Problem

> "How can a spatial data system dynamically intercept standard point-to-point map routing to inject optimized, bike-friendly waypoints—such as repair shops, cafes, and scenic rest stops—based on safety constraints, topographic elevation, and user-defined detour limits within the province of Cavite?"

Most navigation apps optimize for cars — fastest route, shortest time, no regard for safety or scenery. BudolRide Navigator flips that: it prioritizes **safety, elevation awareness, and leisure** for cyclists specifically.

## Features

- 🗺️ **Intelligent Leisure Routing** — set a detour radius (0.5–5 km) and preferred stop types (cafes, scenic views); the route dynamically bends to pass through them.
- 🚫 **Bicycle-First Safety Pathing** — automatically avoids expressways and truck highways (e.g. CAVITEX/SLEX), favoring bike lanes and barangay roads.
- ⛰️ **Topographic ("Ahon") Forecasting** — interactive elevation chart showing steep climbs (>8% gradient) before you ride.
- 🔧 **Emergency Infrastructure Locator** — find the nearest bike repair/vulcanizing shop along your route.

## Tech Stack

| Layer | Technology |
|---|---|
| Mobile App | React Native (Expo) + TypeScript |
| Map Rendering | react-native-maps |
| Backend API | Node.js + Express |
| Database | PostgreSQL + PostGIS ([Supabase](https://supabase.com)) |
| Auth | Supabase Auth |
| Routing Engine | [OSRM](http://project-osrm.org/) (Docker) |
| Data Ingestion (ETL) | Python |
| Backend Hosting | [Render](https://render.com) |
| Mobile Build | Expo EAS Build |

## Data Sources

| Data | Source |
|---|---|
| Roads, bike shops, viewpoints, cafes | [OpenStreetMap](https://wiki.openstreetmap.org/wiki/Overpass_API) via Overpass API |
| Elevation profiles | [OpenTopoData API](https://www.opentopodata.org/) |
| Enriched tourist spot data | [Wikidata Query Service](https://query.wikidata.org/) |

## Project Structure

```
budolride-navigator/
├── frontend/          # React Native (Expo) app
├── backend/           # Node.js + Express API
├── data-engineering/  # Python ETL scripts, PostGIS setup, OSRM config (OSM, elevation, POI data)
├── docs/              # Full project proposal & planning docs
└── AGENTS.md          # AI coding assistant context (Kiro/Copilot/Codex)
```

## Getting Started

> ⚠️ Setup instructions will be filled in as each part is built.

### Prerequisites
- Node.js (LTS)
- Python 3.x (for ETL scripts)
- Docker (for OSRM)
- Expo Go app on your phone (for testing)

### Frontend (Mobile App)
```bash
cd frontend
npx expo start
```
Scan the QR code with Expo Go to run on your device.

### Backend API
```bash
cd backend
npm install
npm run dev
```

### Data Engineering (Routing Engine & ETL)
```bash
cd data-engineering
docker compose up   # OSRM
python etl_script.py # example — run individual ETL scripts as needed
```

## Roadmap / Future Implementation

Not included in v1, planned for later:
- Offline routing
- User-generated POI content (reviews, submissions)
- Live traffic / real-time road conditions
- Multi-user / social features
- Push notifications
- Expansion to NCR (Metro Manila)

## License

Personal project — license to be decided.

## Team

| Name | Role |
|---|---|
| Aaron Angat | Full-Stack Engineer (Backend API & Mobile UI) |
| NCJ Bakx (Nathaniel) | Data Engineer (Data Infrastructure & Routing Engine) |

Built to learn React Native, Node.js, and geospatial data engineering.
