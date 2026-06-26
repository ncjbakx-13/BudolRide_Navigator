import requests
import json

def fetch_cavite_bike_shops():
    """Fetches bicycle shops in Cavite using the OpenStreetMap Overpass API."""
    
    # The Overpass API endpoint
    url = "http://overpass-api.de/api/interpreter"
    
    # Required User-Agent to avoid 406 errors
    headers = {
        'User-Agent': 'budolride-navigator-DataPipeline/1.0 (contact: nathanielcornelisjerardobakx@gmail.com)'
    }
    
    # The query: Find the area of Cavite, then find all nodes tagged as 'shop=bicycle'
    query = """
    [out:json][timeout:25];
    area["name"="Cavite"]["admin_level"="4"]->.searchArea;
    (
      node["shop"="bicycle"](area.searchArea);
      way["shop"="bicycle"](area.searchArea);
    );
    out center;
    """
    
    print("Fetching bike shops in Cavite from OpenStreetMap... Please wait.")
    
    try:
        # Send the request to the API with headers
        response = requests.post(url, data={'data': query}, headers=headers)
        response.raise_for_status() 
        
        data = response.json()
        elements = data.get('elements', [])
        
        print(f"Success! Found {len(elements)} bicycle shops in Cavite.\n")
        
        # Print the first 5 shops as a quick preview
        print("--- SAMPLE DATA ---")
        for i, el in enumerate(elements[:5]):
            name = el.get('tags', {}).get('name', 'Unnamed Shop')
            lat = el.get('lat') or el.get('center', {}).get('lat')
            lon = el.get('lon') or el.get('center', {}).get('lon')
            print(f"{i+1}. {name} | Coordinates: {lat}, {lon}")
            
        print("\nData Extraction Pipeline is working!")
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_cavite_bike_shops()