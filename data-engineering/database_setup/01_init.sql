-- 1. Enable PostGIS (Crucial for storing geographic coordinates)
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Create the table for your map data (Points of Interest)
CREATE TABLE IF NOT EXISTS spatial_pois (
    id SERIAL PRIMARY KEY,
    osm_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(255),
    poi_type VARCHAR(100), -- e.g., 'bicycle_shop', 'cafe'
    geom GEOMETRY(Point, 4326), -- 4326 is the standard GPS coordinate system
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create a spatial index so map searches are lightning-fast
CREATE INDEX IF NOT EXISTS spatial_pois_geom_idx
ON spatial_pois
USING GIST (geom);