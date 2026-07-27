# **Project: "BudolRide Navigator"**

**Topic:** A POI-Aware Bicycle Navigation & Topographic Routing System for Cavite

### **1\. The Problem Statement**

> *"How can a spatial data system dynamically intercept standard point-to-point map routing to inject optimized, bike-friendly waypoints—such as repair shops, cafes, and scenic rest stops—based on safety constraints, topographic elevation, and user-defined detour limits within the province of Cavite?"*

### **2\. How the System Solves the Problem**

*Think of this app as a smart navigation assistant built entirely for bicycle riders, not cars. When a cyclist types in where they want to go, the app doesn’t just pick the fastest highway—instead, it scans the map of Cavite and instantly cuts out dangerous, fast-moving truck highways and expressways, forcing the route onto dedicated bike lanes and quiet neighborhood backroads.*

*Next, the app looks at how much extra time the rider wants to spend exploring or resting (their chosen "detour limit"). It draws an invisible safety corridor around the route and automatically finds highly rated coffee shops, scenic overlooks, or emergency bike repair shops sitting just off the main path. It then smoothly bends the route to connect these stops together into one seamless, stress-free trip. Finally, it checks local mountain and hill data to create a simple chart showing exactly where the steep uphill climbs are before the rider even starts pedaling, ensuring they are never caught off guard by a brutal hill.*

### **3\. What Our App Will Do (Core Features)**

* **Intelligent Leisure Routing (The Main Selling Point):** The app goes beyond finding the fastest path. Cyclists can input a "Detour Radius" (e.g., 2 kilometers) and select preferred stops (e.g., Cafes, Scenic Views). The algorithm dynamically curves the route to seamlessly pass through these high-rated points of interest.  
* **Bicycle-First Safety Pathing:** The routing engine automatically penalizes major truck highways and strictly bans expressways (like CAVITEX/SLEX), forcing the route onto dedicated bike lanes, barangay roads, and safe residential streets.  
* **Topographic ("Ahon") Forecasting:** The app renders an interactive elevation chart beneath the map. Before pedaling, cyclists can see exactly where the steepest climbs (gradients \> 8%) are located along their custom route.  
* **Emergency Infrastructure Locator:** Cyclists can instantly locate the nearest verified bicycle repair or vulcanizing shops within a set radius of their active travel path.

### **4\. Tools That Will Be Used (100% Free Stack)**

**For the Data Engineer — Nathaniel (NCJ Bakx) (Data Infrastructure & Routing Engine):**

* **Python:** Core scripting language for building automated ETL (Extract, Transform, Load) data ingestion pipelines.  
* **PostgreSQL with PostGIS:** The industry-standard spatial database. It natively handles geographic coordinates (`GeoJSON`) and calculates complex spatial logic (like geographic buffer zones and distance bounding) at lightning speed.  
* **OSRM (Open Source Routing Machine):** An open-source geographic routing engine hosted locally via Docker. The Data Engineer will configure its **Lua scripts** to prioritize bike lanes and heavily penalize dangerous vehicle roads.

**For the Software / Full-Stack Engineer — Aaron Angat (Backend API & Mobile UI):**

* **Node.js with Express** (or Fastify) — handles REST API endpoints, runs spatial SQL queries against PostGIS, and serves JSON to the mobile app.  
* **React Native (with Expo)** — builds the mobile app for Android \+ iOS from one codebase, using JavaScript/TypeScript.  
* **react-native-maps** — renders the interactive map, custom route polylines, and markers, using free map tiles (or Google Maps/Apple Maps native rendering depending on config) without needing a paid API tier for basic use.

### **5\. Data That Will Be Gathered & Respective Links**

The Data Engineer will build automated Python scripts to pull data from these free, developer-friendly platforms:

**A. Spatial Data (Roads, Bike Shops, Viewpoints, Cafes)**

* **Source:** OpenStreetMap (OSM) via the Overpass API  
* **Documentation Link:** [https://wiki.openstreetmap.org/wiki/Overpass\_API](https://wiki.openstreetmap.org/wiki/Overpass_API)  
* **Testing Tool (Overpass Turbo):** [https://overpass-turbo.eu/](https://overpass-turbo.eu/)

**B. Topographic Data (Elevation Profiles)**

* **Source:** OpenTopoData API  
* **Documentation Link:** [https://www.opentopodata.org/](https://www.opentopodata.org/)

**C. Enriched Tourist Spot Data (Optional for UI enrichment)**

* **Source:** Wikidata Query Service  
* **Documentation Link:** [https://query.wikidata.org/](https://query.wikidata.org/)

### **6\. Deployment & Hosting**

The stack below prioritizes free tiers and beginner-friendly tools.

**Database (PostgreSQL \+ PostGIS)**

* **Supabase** — hosted PostgreSQL with one-click PostGIS extension. Free tier includes \~500MB storage (pauses after inactivity, wakes on next request).

**Authentication**

* **Supabase Auth** — built into Supabase, supports email/password and social login (e.g., Google). No separate auth service needed since the database is already on Supabase.

**Backend API Hosting (Node.js)**

* **Render** — free tier for Node.js web services. Free tier sleeps after inactivity and takes \~30–60 seconds to wake on the next request; acceptable for a personal/learning-stage project.

**Routing Engine (OSRM)**

* Runs locally via Docker during development.  
* For later 24/7 hosting, Render also supports Docker deployments, though free-tier RAM limits may be tight depending on the size of Cavite's map data loaded.

**Mobile App Distribution**

* **Expo / EAS Build** — handles building the installable app; no separate hosting needed. Development/testing done live via the Expo Go app.

### **7\. Repository Structure**

* **frontend/** — React Native (Expo) app — Aaron Angat  
* **backend/** — Node.js \+ Express API — Aaron Angat  
* **data-engineering/** — Python ETL scripts, PostGIS setup, OSRM config — Nathaniel (NCJ Bakx)  
* **docs/** — full project proposal & planning docs

### **8\. Future Implementation**

The following features are not included in v1 but may be added in future versions:

* **Expansion to NCR (Metro Manila)** — v1 is scoped to Cavite province only; expanding coverage to NCR would require additional OSM/topographic data ingestion and route-engine reconfiguration for that region.   
* **Offline routing** — no offline map caching or offline navigation support in v1; requires an active internet connection.  
* **User-generated content** — POI data (cafes, repair shops, scenic spots) is sourced entirely from OpenStreetMap/Wikidata for v1; no in-app user reviews, ratings, or POI submissions yet.  
* **Live traffic or real-time road conditions** — routing is based on static map and elevation data, not live traffic feeds.  
* **Multi-user / social features** — no shared rides, friend tracking, or leaderboards in v1.  
* **Push notifications** — no proactive alerts (e.g., weather, road closures) in v1.