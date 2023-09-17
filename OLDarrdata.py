import requests
import json
import time
import datetime

# Authentication credentials
USERNAME = "jo.stillawake"
PASSWORD = "Uk9w7uPP!H@4TVC"

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
end_time = current_time
start_time = end_time - 86400

flights_data = get_flights_data(AIRPORT_ICAO, start_time, end_time)
save_to_daily_file(flights_data)


print(f"Start time: {datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
print(f"End time: {datetime.datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")
