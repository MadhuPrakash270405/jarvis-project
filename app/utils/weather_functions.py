import sqlite3
import os
import requests
from datetime import datetime, timedelta
import re


import json
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
# Replace with your OpenWeatherMap API key

DB_PATH='weather_cache.db'

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_cache (
            date TEXT,
            location TEXT,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (date, location)
        )
    """
    )
    conn.commit()
    conn.close()


setup_database()


def get_cached_weather(date, location):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT data FROM weather_cache WHERE date = ? AND location = ?",
        (date, location),
    )
    result = cursor.fetchone()
    conn.close()
    return json.loads(result[0]) if result else None


def cache_weather(date, location, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO weather_cache (date, location, data) VALUES (?, ?, ?)",
        (date, location, json.dumps(data)),
    )
    conn.commit()
    conn.close()


def check_weather_type(dateStr):
    given_date = datetime.strptime(dateStr, "%Y-%m-%d").date()
    current_date = datetime.now().date()
    # print({"given_date": given_date, "current_date": current_date})
    if given_date == current_date:
        return "current"
    if given_date < current_date:
        return "history"
    else:
        return "forecast"


def weather_for_one_week(location):
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    for i in range(7):
        specific_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        specific_date_weather(specific_date, location)
        print("============================================================")


def specific_date_weather(specific_date, location):
    weather_type = check_weather_type(specific_date)
    endpoint = (
        "current"
        if weather_type == "current"
        else "forecast"
        if weather_type == "forecast"
        else "history"
    )
    cached_weather = get_cached_weather(specific_date, location)
    if cached_weather:
        print(f"Using cached data for {specific_date} in {location}")
        data = cached_weather
    else:
        url = f"http://api.weatherapi.com/v1/{endpoint}.json?key={api_key}&q={location}"
        if weather_type != "current":
            url += f"&dt={specific_date}"

        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            cache_weather(specific_date, location, data)
        else:
            print(f"Failed to retrieve data: {data}")
            return

    # Print the weather details
    if weather_type == "current":
        return print_current_weather(data, location)
    else:
        return print_forecast_or_history_weather(data, specific_date, location, weather_type)

def print_current_weather(data, location):
    try:
        current_temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        print(f"Current weather in {location}: Temperature: {current_temp}°C, Condition: {condition}")
        return(f"Current weather in {location}: Temperature: {current_temp}°C, Condition: {condition}")
    
    except KeyError as e:
        print(f"Error retrieving current weather data for {location}: {e}")
        return(f"Error retrieving current weather data for {location}: {e}")

def print_forecast_or_history_weather(data, specific_date, location, weather_type):
    try:
        if "forecast" in data and len(data["forecast"]["forecastday"]) > 0:
            weather_data = data["forecast"]["forecastday"][0]
            max_temp = weather_data["day"]["maxtemp_c"]
            min_temp = weather_data["day"]["mintemp_c"]
            condition = weather_data["day"]["condition"]["text"]
            weather_desc = "forecast" if weather_type == "forecast" else "historical"
            print(f"On {specific_date}, the {weather_desc} weather in {location} was: Max Temperature: {max_temp}°C, Min Temperature: {min_temp}°C, Condition: {condition}")
            return(f"On {specific_date}, the {weather_desc} weather in {location} was: Max Temperature: {max_temp}°C, Min Temperature: {min_temp}°C, Condition: {condition}")
        
        else:
            print(f"No {weather_type} data available for {specific_date} in {location}")
            return(f"No {weather_type} data available for {specific_date} in {location}")

    except KeyError as e:
        print(f"Error retrieving {weather_type} weather data for {location} on {specific_date}: {e}")
        return(f"Error retrieving {weather_type} weather data for {location} on {specific_date}: {e}")

def parse_weather_command(command):
    command = command.lower()
    # Updated regular expression patterns for different commands
    current_weather_pattern = r"what'?s the weather (like )?in ([\w\s]+)|weather (in|for) ([\w\s]+)"
    forecast_weather_pattern = r"what'?s the weather (like )?for the next (week|7 days) in ([\w\s]+)|forecast (for )?the next (week|7 days) in ([\w\s]+)"
    specific_date_pattern = r"weather on (\d{4}-\d{2}-\d{2}) in ([\w\s]+)|forecast for (\d{4}-\d{2}-\d{2}) in ([\w\s]+)"
    date_range_pattern = r"weather from (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) in ([\w\s]+)|forecast from (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2}) in ([\w\s]+)"

    match = re.search(current_weather_pattern, command)
    if match:
        # The location can be in either group 2 or 4 depending on the pattern matched
        location = match.group(2) or match.group(4)
        return {"type": "current", "location": location}

    match = re.search(forecast_weather_pattern, command)
    if match:
        # The location can be in either group 3 or 6
        location = match.group(3) or match.group(6)
        return {"type": "forecast", "location": location}

    match = re.search(specific_date_pattern, command)
    if match:
        # The date and location can be in different groups
        date = match.group(1) or match.group(3)
        location = match.group(2) or match.group(4)
        return {"type": "specific_date", "date": date, "location": location}

    match = re.search(date_range_pattern, command)
    if match:
        # The dates and location can be in different groups
        start_date = match.group(1) or match.group(4)
        end_date = match.group(2) or match.group(5)
        location = match.group(3) or match.group(6)
        return {"type": "date_range", "start_date": start_date, "end_date": end_date, "location": location}

    return None


def handle_weather_command(command):
    print(f"Handling weather command: {command}")
    parsed_command = parse_weather_command(command)
    print(parsed_command)
    if parsed_command:
        if parsed_command["type"] == "current":
            return specific_date_weather(datetime.now().strftime("%Y-%m-%d"), parsed_command["location"])
        elif parsed_command["type"] == "forecast":
            return weather_for_one_week(parsed_command["location"])
        elif parsed_command["type"] == "specific_date":
            return specific_date_weather(parsed_command["date"], parsed_command["location"])

    else:
        return("Sorry, I didn't understand that command.")


# location = "London"
# weather_for_one_week(location)
voice_command = "what is the weather in New York?"  # This would come from your speech-to-text module
handle_weather_command(voice_command)
# voice_command = "what is the weather on 2023-12-25 in New York"
# handle_weather_command(voice_command)
# specific_date_weather("2023-11-18", location)
