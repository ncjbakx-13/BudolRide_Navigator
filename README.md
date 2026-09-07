# 🚴 BudolRide Navigator

A POI-aware bicycle navigation and topographic-routing app for cyclists in Cavite, Philippines.

Unlike typical car-first navigation apps, BudolRide Navigator routes cyclists onto **safe bike lanes and backroads**, can detour through cafes, repair shops, or scenic stops, and shows elevation climbs before the ride starts.

> 📌 A two-person team project for learning React Native, FastAPI, and geospatial data engineering.

## The Problem

> How can a spatial data system dynamically intercept standard point-to-point map routing to inject optimized, bike-friendly waypoints—such as repair shops, cafes, and scenic rest stops—based on safety constraints, topographic elevation, and user-defined detour limits within the province of Cavite?

Most navigation apps optimize for cars: fastest route, shortest time, and little regard for safety or scenery. BudolRide Navigator prioritizes safety, elevation awareness, and leisure for cyclists.

## Features

- 🗺️ **Intelligent Leisure Routing** — Set a detour radius (0.5–5 km) and preferred stop types; the route can pass through suitable points of interest.
- 🚫 **Bicycle-First Safety Pathing** — Avoid expressways and truck highways (such as CAVITEX and SLEX), favoring bike lanes and barangay roads.
- ⛰️ **Topographic ("Ahon") Forecasting** — Show an interactive elevation chart and identify steep climbs (over 8% gradient) before a ride.
- 🔧 **Emergency Infrastructure Locator** — Find the nearest bike repair or vulcanizing shop along a route.

## Tech Stack

| Layer | Technology |
|---|---|
| Mobile App | React Native (Expo) + TypeScript |
| Map Rendering | react-native-maps |
| Backend API | Python + FastAPI |
| API Validation & Documentation | Pydantic + FastAPI OpenAPI/Swagger |
| Database | PostgreSQL + PostGIS (Supabase) |
| Database Access | SQLAlchemy + GeoAlchemy2 |
| Database Migrations | Alembic |
| Auth | Supabase Auth (JWT validated by FastAPI) |
| Routing Engine | OSRM (Docker) |
| Data Ingestion (ETL) | Python |
| Backend Hosting | Render |
| Mobile Build | Expo EAS Build |

## Data Sources

| Data | Source |
|---|---|
| Roads, bike shops, viewpoints, cafes | [OpenStreetMap](https://wiki.openstreetmap.org/wiki/Overpass_API) via Overpass API |
| Elevation profiles | [OpenTopoData API](https://www.opentopodata.org/) |
| Enriched tourist-spot data | [Wikidata Query Service](https://query.wikidata.org/) |

## Project Structure

```text
budolride-navigator/
├── frontend/          # React Native (Expo) app
├── backend/           # FastAPI application and API tests
├── data-engineering/  # Python ETL scripts, PostGIS setup, and OSRM configuration
├── docs/              # Full project proposal and planning documents
└── README.md
```

## Engineering Documentation

These documents separate confirmed product decisions from planned work and should be
read before adding application features:

- [Architecture baseline](docs/ARCHITECTURE.md)
- [Decisions and open questions](docs/DECISIONS.md)
- [Engineering standards](docs/ENGINEERING_STANDARDS.md)
- [Security baseline](docs/SECURITY.md)
- [Data operations](docs/DATA_OPERATIONS.md)
- [Delivery plan](docs/DELIVERY_PLAN.md)
- [API contract baseline](docs/API_CONTRACT.md)
- [Test strategy](docs/TEST_STRATEGY.md)
- [Project glossary](docs/GLOSSARY.md)

## Getting Started

> ⚠️ Detailed setup instructions will be added as each component is built.

### Prerequisites

- Node.js (LTS)
- Python 3.12+
- Docker Desktop (for OSRM)
- Expo Go on a phone for device testing

### Frontend (Mobile App)

```bash
cd frontend
npx expo start
```

Scan the QR code with Expo Go to run the app on a device.

### Backend API

Create and activate a virtual environment, then install the backend dependencies:

```bash
cd backend
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies and start the development server:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

When running, FastAPI's interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### Data Engineering (Routing Engine & ETL)

```bash
cd data-engineering
docker compose up    # OSRM
python etl_script.py # Run individual ETL scripts as needed
```

## Roadmap

Not included in v1, planned for later:

- Offline routing
- User-generated POI content (reviews and submissions)
- Live traffic and real-time road conditions
- Multi-user and social features
- Push notifications
- Expansion to Metro Manila

## License

Personal project — license to be decided.

## Team

| Name | Role |
|---|---|
| Aaron Angat | Full-Stack Engineer (FastAPI backend and mobile UI) |
| NCJ Bakx (Nathaniel) | Data Engineer (data infrastructure and routing engine) |

Built to learn React Native, FastAPI, and geospatial data engineering.
