import logging
import os
import time
from pathlib import Path

import psycopg2
import requests
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

LOGGER = logging.getLogger(__name__)
OVERPASS_URL = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
OVERPASS_USER_AGENT = os.getenv(
    "OVERPASS_USER_AGENT", "BudolRide-Navigator-ETL/0.1 (local-development)"
)


def get_database_url() -> str:
    """Read the ETL connection string without ever embedding credentials in source."""
    database_url = os.getenv("BUDOLRIDE_DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "BUDOLRIDE_DATABASE_URL is required. Copy .env.example to .env and set it locally."
        )
    return database_url

def fetch_and_store_bike_shops():
    """Fetches bicycle shops in Cavite and saves them to PostGIS."""
    
    headers = {"User-Agent": OVERPASS_USER_AGENT}

    query = """
    [out:json][timeout:90];
    area["name"="Cavite"]["admin_level"="4"]->.searchArea;
    (
      node["shop"="bicycle"](area.searchArea);
      way["shop"="bicycle"](area.searchArea);
    );
    out center;
    """
    
    print("Fetching bike shops in Cavite from OpenStreetMap... (This might take a minute)")
    
    try:
        max_retries = 3
        elements = []

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    OVERPASS_URL,
                    data={"data": query},
                    headers=headers,
                    timeout=(10, 100),
                )
                response.raise_for_status()
                payload = response.json()
                elements = payload.get("elements", [])
                break
            except (requests.exceptions.RequestException, ValueError) as error:
                print(f"API Attempt {attempt + 1} failed: {error}")
                if attempt < max_retries - 1:
                    retry_delay = 2 ** attempt
                    print(f"Server busy. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. The OSM server is currently overloaded. Please try again later.")
                    return

        if not elements:
            print("No bicycle shops found.")
            return

        print(f"Found {len(elements)} bicycle shops! Connecting to database...")

        inserted_count = 0
        with psycopg2.connect(get_database_url(), connect_timeout=10) as conn:
            with conn.cursor() as cursor:
                for element in elements:
                    osm_id = element.get("id")
                    name = element.get("tags", {}).get("name", "Unnamed Shop")
                    # Nodes have direct coordinates; ways use the Overpass center.
                    lat = element.get("lat") or element.get("center", {}).get("lat")
                    lon = element.get("lon") or element.get("center", {}).get("lon")

                    if lat is not None and lon is not None:
                        insert_query = """
                            INSERT INTO spatial_pois (osm_id, name, poi_type, geom)
                            VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                            ON CONFLICT (osm_id) DO NOTHING;
                        """
                        cursor.execute(insert_query, (osm_id, name, "bicycle_shop", lon, lat))
                        inserted_count += cursor.rowcount

        print(f"Success! {inserted_count} new bike shops were safely saved to PostGIS.")
        print("Data Pipeline Complete!")

    except (RuntimeError, psycopg2.Error):
        LOGGER.error("POI ingestion could not complete; review local configuration and logs.")

if __name__ == "__main__":
    fetch_and_store_bike_shops()
