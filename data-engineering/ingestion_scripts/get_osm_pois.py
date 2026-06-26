import requests
import psycopg2
import time

def fetch_and_store_bike_shops():
    """Fetches bicycle shops in Cavite and saves them to PostGIS."""
    
    # 1. Database Connection Details
    db_params = {
        "dbname": "budolride_db",
        "user": "postgres",
        "password": "Nathanielbakx04@#$!", # <-- BE SURE TO CHANGE THIS
        "host": "localhost",
        "port": "5432"
    }
    
    # 2. OpenStreetMap API Setup
    url = "http://overpass-api.de/api/interpreter"
    headers = {'User-Agent': 'BudolRide-DataPipeline/1.0'}
    
    # The query: Increased timeout to 90 seconds
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
        # 3. Get Data from API with Robust Retry Logic
        max_retries = 3
        elements = []
        
        for attempt in range(max_retries):
            try:
                # Added a 100-second timeout to the Python request itself
                response = requests.post(url, data={'data': query}, headers=headers, timeout=100)
                response.raise_for_status() 
                elements = response.json().get('elements', [])
                break # Success! Break out of the retry loop
            except requests.exceptions.RequestException as e:
                print(f"API Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    print("Server busy. Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print("Max retries reached. The OSM server is currently overloaded. Please try again later.")
                    return
                    
        if not elements:
            print("No bicycle shops found.")
            return

        print(f"Found {len(elements)} bicycle shops! Connecting to database...")
        
        # 4. Connect to PostGIS Database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # 5. Insert Data into Database
        inserted_count = 0
        for el in elements:
            osm_id = el.get('id')
            name = el.get('tags', {}).get('name', 'Unnamed Shop')
            # Handle both node (direct lat/lon) and way (center lat/lon) coordinates
            lat = el.get('lat') or el.get('center', {}).get('lat')
            lon = el.get('lon') or el.get('center', {}).get('lon')
            
            if lat and lon:
                # SQL Query using PostGIS functions to create a GEOMETRY point
                insert_query = """
                    INSERT INTO spatial_pois (osm_id, name, poi_type, geom)
                    VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                    ON CONFLICT (osm_id) DO NOTHING;
                """
                cursor.execute(insert_query, (osm_id, name, 'bicycle_shop', lon, lat))
                inserted_count += cursor.rowcount
                
        # 6. Save changes and close connection
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Success! {inserted_count} new bike shops were safely saved to PostGIS.")
        print("Data Pipeline Complete!")
        
    except Exception as e:
        print(f"A database error occurred: {e}")

if __name__ == "__main__":
    fetch_and_store_bike_shops()