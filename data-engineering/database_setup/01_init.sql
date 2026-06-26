-- This script initializes your spatial database when it first boots up.
-- It enables PostGIS and creates your first table for the Cavite map data.

-- 1. Enable the PostGIS extension for spatial mapping
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Create the table to hold Cafes, Scenic Spots, and Repair Shops
CREATE TABLE IF NOT EXISTS spatial_pois (
    id SERIAL PRIMARY KEY,
    osm_id BIGINT UNIQUE,
    name VARCHAR(255),
    category VARCHAR(50), -- e.g., 'bicycle_shop', 'cafe', 'viewpoint'
    geom GEOMETRY(Point, 4326) -- The spatial column that holds longitude/latitude
);

-- Note: We will add more tables later for routes and elevation, 
-- but this is the perfect starting point for your POI ingestion script.