import requests
import json

# Define the API endpoint and parameters
api_key = 'cd2ebdbf19f640a69c359af826102d65'  # Replace with your actual API key
base_url = 'https://api.sportsdata.io/v3/cbb/odds/json/MatchupTrends'

# Input team abbreviations
team = 'UCONN'  # Replace with the abbreviation of the requested team
opponent = 'MARQ'  # Replace with the abbreviation of the opponent team

# Construct the full API URL
url = f"{base_url}/{team}/{opponent}?key={api_key}"

# Function to fetch matchup trends data
def fetch_matchup_trends(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()  # Successfully fetched data

            # Print raw data for debugging
            print("Raw API Response:")
            print(json.dumps(data, indent=4))

            return data  # Return all the data without filtering
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None  # Return None if API request fails
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to save raw JSON data to a file
def save_to_json(data, filename="matchup_trends.json"):
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON data saved to {filename}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

# Fetch data
all_data = fetch_matchup_trends(url)

# Save raw JSON data to a file (only if valid data exists)
if all_data:
    save_to_json(all_data, filename="matchup_trends.json")
else:
    print("No valid data to save.")
