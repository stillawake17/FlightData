import requests
import json
import time
import datetime
import os

# ... [Your existing functions here] ...
def get_json_files_in_directory():
    # Get a list of all files in the current directory with a .json extension
    return [file for file in os.listdir() if file.endswith('.json')]

print("Current Working Directory:", os.getcwd())

with open("config.json", "r") as file:
    config = json.load(file)

USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]


# URL and Parameters
BASE_URL = "https://opensky-network.org/api/flights"
AIRPORT_ICAO = "EGGD"

def get_flights_data(airport_icao, start_time, end_time):
    url = f"{BASE_URL}/arrival?airport={airport_icao}&begin={start_time}&end={end_time}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def save_to_daily_file(data):
    existing_data = []
    filename = f"flights_data_{datetime.datetime.now().strftime('%Y_%m_%d')}.json"
    
    # Load existing data
    try:
        with open(filename, "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist yet

    # Generate a set of unique identifiers for existing data
    unique_data_identifiers = {f"{flight['icao24']}_{flight['firstSeen']}_{flight['lastSeen']}" for flight in existing_data}

    # Filter out duplicates from new data
    unique_new_data = [flight for flight in data if f"{flight['icao24']}_{flight['firstSeen']}_{flight['lastSeen']}" not in unique_data_identifiers]

    # Combine existing and new data
    combined_data = existing_data + unique_new_data

    with open(filename, "w") as file:
        json.dump(combined_data, file)

# Calculate timestamps dynamically
current_time = int(time.time())
start_of_year = datetime.datetime(datetime.datetime.now().year, 1, 1)
start_of_year_timestamp = int(time.mktime(start_of_year.timetuple()))

# Loop from the start of the year to the current time in 6-day intervals
for end_time in range(current_time, start_of_year_timestamp, -6 * 86400):
    start_time = max(end_time - 6 * 86400, start_of_year_timestamp)  # Ensure start_time is not before start of the year

    flights_data = get_flights_data(AIRPORT_ICAO, start_time, end_time)
    save_to_daily_file(flights_data)

    print(f"Start time: {datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"End time: {datetime.datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")

# ... [Rest of your code] ...
def combine_json_files(json_files):
    all_data = []

    # Load data from each file into the all_data list
    for file in json_files:
        with open(file, 'r') as f:
            data = json.load(f)
            # Check if the loaded data is a list of dictionaries
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                all_data.extend(data)

    # Remove duplicates based on the unique identifier
    unique_data_identifiers = set()
    unique_data = []
    for flight in all_data:
        identifier = f"{flight['icao24']}_{flight['firstSeen']}_{flight['lastSeen']}"
        if identifier not in unique_data_identifiers:
            unique_data_identifiers.add(identifier)
            unique_data.append(flight)

    # Save the combined unique data to a new file
    with open("combined_flights_data.json", "w") as f:
        json.dump(unique_data, f)

    print(f"Combined data saved to combined_flights_data.json with {len(unique_data)} unique flights.")


# After finishing the loop, combine the JSON files
json_files = get_json_files_in_directory()
#print("\nAvailable JSON files:")
for file in json_files:
    print(file)

# Combine the data from all JSON files and save to a new file
combine_json_files(json_files)
