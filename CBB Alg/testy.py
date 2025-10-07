import requests

# Define the API endpoint and parameters
api_key = 'cd2ebdbf19f640a69c359af826102d65'  # Replace with your actual API key
base_url = 'https://api.sportsdata.io/v3/cbb/odds/json/MatchupTrends'

# Input team abbreviations
team = 'STLOU'  # Replace with the abbreviation of the requested team
opponent = 'DAY'  # Replace with the abbreviation of the opponent team

# Construct the full API URL
url = f"{base_url}/{team}/{opponent}?key={api_key}"

# Make the request
response = requests.get(url)

# Print raw response
print("Status Code:", response.status_code)
print("Raw Response:", response.text)
