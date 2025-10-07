import requests
import json

# Define the API endpoint and parameters
team = 'STLOU'  # Use the team abbreviation, e.g., 'OU' for Oklahoma
key = 'cd2ebdbf19f640a69c359af826102d65'  # Your API key
url = f'https://api.sportsdata.io/v3/cbb/odds/json/TeamTrends/{team}?key={key}'

# Function to fetch team trends data
def fetch_team_trends(api_url):
    try:
        # Send the GET request to the API
        response = requests.get(api_url)

        # Check the response status
        if response.status_code == 200:
            # Parse the response as JSON
            data = response.json()
            print("\n--- Team Trends Data ---\n")
            print(json.dumps(data, indent=4))  # Pretty-print the JSON data
        else:
            # Print an error message if the request is unsuccessful
            print(f"Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        print(f"An error occurred: {e}")

# Call the function
fetch_team_trends(url)
