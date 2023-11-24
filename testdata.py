import requests
import json
import os
import time
from datetime import datetime

# Function to get a list of all .json files in the current directory
def get_json_files_in_directory():
    return [file for file in os.listdir() if file.endswith('.json')]

# Function to get flight data from the OpenSky API
def get_flights_data(airport_icao, start_time, end_time, flight_type="arrival"):
    url = f"{BASE_URL}/{flight_type}?airport={airport_icao}&begin={start_time}&end={end_time}"
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

# Function to save data to a daily file
def save_to_daily_file(data, filename):
    try:
        with open(filename, "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Generate a set of unique identifiers for existing data
    unique_data_identifiers = {f"{flight['icao24']}_{flight['firstSeen']}_{flight['lastSeen']}" for flight in existing_data}
    
    # Filter out duplicates from new data
    unique_new_data = [flight for flight in data if f"{flight['icao24']}_{flight['firstSeen']}_{flight['lastSeen']}" not in unique_data_identifiers]
    
    # Combine existing and new data
    combined_data = existing_data + unique_new_data
    
    with open(filename, "w") as file:
        json.dump(combined_data, file)

def combine_json_files_fixed(json_files):
    all_data = []
    unique_data_identifiers = set()

    for file_name in json_files:
        with open(file_name, 'r') as f:
            data = json.load(f)
        if isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # Update the unique identifiers set with the current file's data before extending the all_data list
            for flight in data:
                identifier = f"{flight['icao24']}_{flight['firstSeen']}_{flight['lastSeen']}"
                if identifier not in unique_data_identifiers:
                    unique_data_identifiers.add(identifier)
                    all_data.append(flight)

    # Now all_data only has unique flights, so there's no need to filter again
    combined_filename = "combined_flights_data.json"
    with open(combined_filename, 'w') as file:
        json.dump(all_data, file)
    print(f"Combined data saved to {combined_filename} with {len(all_data)} unique flights.")


# Function to combine JSON files into one
# def combine_json_files(json_files):
#     all_data = []
#     unique_data_identifiers = set()

#     for file_name in json_files:
#         with open(file_name, 'r') as f:
#             data = json.load(f)
#         if isinstance(data, list) and all(isinstance(item, dict) for item in data):
#             all_data.extend(data)



#     # Remove duplicates based on the unique identifier
#     unique_data = [flight for flight in all_data if f"{flight['icao24']}_{flight['firstSeen']}_{flight['lastSeen']}" not in unique_data_identifiers]
#     unique_data_identifiers.update(f"{flight['icao24']}_{flight['firstSeen']}_{flight['lastSeen']}" for flight in unique_data)

#     # Save the combined unique data to a new file
#     combined_filename = "combined_flights_data.json"
#     with open(combined_filename, 'w') as file:
#         json.dump(unique_data, file)
#     print(f"Combined data saved to {combined_filename} with {len(unique_data)} unique flights.")

# Load configuration from file
with open("config.json", "r") as file:
    config = json.load(file)

USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]

# URL and Parameters
BASE_URL = "https://opensky-network.org/api/flights"
AIRPORT_ICAO = "EGGD"

# Main code
current_time = int(time.time())
end_time = current_time - (327 * 86400)   # 5 days ago
start_time = end_time - (6 * 86400)      # 6 days before that

# Fetch and save arrival data
arrivals = get_flights_data(AIRPORT_ICAO, start_time, end_time, "arrival")
arrival_filename = f"arrivals_data_{datetime.now().strftime('%Y_%m_%d')}.json"
save_to_daily_file(arrivals, arrival_filename)

# Fetch and save departure data
departures = get_flights_data(AIRPORT_ICAO, start_time, end_time, "departure")
departure_filename = f"departures_data_{datetime.now().strftime('%Y_%m_%d')}.json"
save_to_daily_file(departures, departure_filename)

# Combine and save all flight data
json_files = get_json_files_in_directory()
combine_json_files_fixed(json_files)

# Convert to human-readable time
human_readable_time = datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')

print(human_readable_time)


