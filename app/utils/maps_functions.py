import time
from urllib.parse import quote
import requests
import os
import json
from dotenv import load_dotenv
import sqlite3
import re

# Load the .env file
load_dotenv()
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
print(google_maps_api_key)

DB_PATH='maps_cache.db'
print(DB_PATH)

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS geocache (
            place_name TEXT PRIMARY KEY,
            coordinates TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS routecache (
            start_place TEXT,
            end_place TEXT,
            route_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (start_place, end_place)
        )
    """
    )
    conn.commit()
    conn.close()


setup_database()


def get_coordinates_from_cache(place_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT coordinates FROM geocache WHERE place_name = ?", (place_name,)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def cache_coordinates(place_name, coordinates):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO geocache (place_name, coordinates) VALUES (?, ?)",
        (place_name, coordinates),
    )
    conn.commit()
    conn.close()


def get_coordinates(place_name):
    # Check cache first
    cached_coordinates = get_coordinates_from_cache(place_name)
    if cached_coordinates:
        return cached_coordinates

    # If not in cache, make API request
    time.sleep(8)
    encoded_place_name = quote(place_name)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded_place_name}&key={google_maps_api_key}"
    response = requests.get(url)
    if response.status_code == 200 and "results" in response.json():
        results = response.json()["results"]
        if results:
            location = results[0]["geometry"]["location"]
            coordinates = f'{location["lat"]},{location["lng"]}'
            cache_coordinates(place_name, coordinates)  # Cache the result
            return coordinates
        else:
            print(f"No results found for {place_name}")
    else:
        print(f"Failed to get coordinates for {place_name}")
    return None


def get_route_from_cache(start_place, end_place):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT route_data FROM routecache WHERE start_place = ? AND end_place = ?",
        (start_place, end_place),
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def cache_route(start_place, end_place, route_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO routecache (start_place, end_place, route_data) VALUES (?, ?, ?)",
        (start_place, end_place, route_data),
    )
    conn.commit()
    conn.close()


def get_route_directions(start_place, end_place):
    # Check cache first
    cached_route = get_route_from_cache(start_place, end_place)
    if cached_route:
        print("Using cached data")
        route = json.loads(cached_route)  # Deserialize the cached route data
    else:
        # If not in cache, make API request
        start_coordinates = get_coordinates(start_place)
        end_coordinates = get_coordinates(end_place)
        if start_coordinates and end_coordinates:
            url = f"https://maps.googleapis.com/maps/api/directions/json?origin={start_coordinates}&destination={end_coordinates}&key={google_maps_api_key}"
            response = requests.get(url)
            if response.status_code == 200 and "routes" in response.json():
                routes = response.json()["routes"]
                if routes:
                    route = routes[0]
                    route_data = json.dumps(route)  # Serialize route data
                    cache_route(start_place, end_place, route_data)  # Cache the result
                else:
                    print("No route found.")
                    return "No route found."
            else:
                print("Failed to retrieve the route directions.")
                return "Failed to retrieve the route directions."
        else:
            print("Failed to get coordinates for start or end place.")
            return "Failed to get coordinates for start or end place."

    # Extract and print distance and duration
    if "legs" in route and route["legs"]:
        leg = route["legs"][0]
        distance = leg["distance"]["text"]
        duration = leg["duration"]["text"]
        print(f"Distance: {distance}")
        print(f"Duration: {duration}")
        return f'Distance Between {start_place} and {end_place} is {distance} and it will take {duration} to reach.' 

    else:
        print("Route data is incomplete.")
        return "Route data is incomplete."


# start_place = "Cleveland, OH"
# end_place = "Los Angeles, CA"
# get_route_directions(start_place, end_place)

def parse_maps_command(command):
    command = command.lower()

    # Pattern for getting directions
    directions_pattern = r"get (?:distance|direction|directions) (?:from|between) (.+?) to (.+)"
    match = re.search(directions_pattern, command)
    if match:
        return {"type": "directions", "start": match.group(1), "end": match.group(2)}

    # Pattern for getting coordinates
    coordinates_pattern = r"get coordinates of (.+)"
    match = re.search(coordinates_pattern, command)
    if match:
        return {"type": "coordinates", "place": match.group(1)}

    return None


def handle_maps_voice_command(command):
    parsed_command = parse_maps_command(command)
    print(parsed_command)
    if parsed_command:
        if parsed_command["type"] == "directions":
            return get_route_directions(parsed_command["start"], parsed_command["end"])
        elif parsed_command["type"] == "coordinates":
            coordinates = get_coordinates(parsed_command["place"])
            if coordinates:
                return f"The coordinates of {parsed_command['place']} are {coordinates}"
            return f'Could not find coordinates for {parsed_command["place"]}'
        else:
            return "Command not recognized."
    else:
        return "Could not parse command."

# Example usage
# voice_command = "get directions from Cleveland, OH to Los Angeles, CA"
# result = handle_maps_voice_command(voice_command)
# print(result)

# voice_command = "get coordinates of New York"
# result = handle_maps_voice_command(voice_command)
# print(result)
