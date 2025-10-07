import os
import requests
import csv

# Get the current working directory
current_directory = os.getcwd()

# Define the API endpoint and parameters
key = 'cd2ebdbf19f640a69c359af826102d65'  # Your API key
url = f'https://api.sportsdata.io/v3/cbb/scores/json/TeamsBasic?key={key}&format=json'

# Send the GET request to the API
response = requests.get(url)

# Check the response status
if response.status_code == 200:
    # If the request is successful, process the response
    teams_info = response.json()

    # Extract the relevant fields for all teams
    teams = [
        {'TeamID': team['TeamID'], 'Key': team['Key'], 'School': team['School']}
        for team in teams_info
    ]

    # Path to save the CSV file in the current working directory
    csv_file_path = os.path.join(current_directory, 'teams_info.csv')

    # Save the data to a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['TeamID', 'Key', 'School']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for team in teams:
            writer.writerow(team)

    print(f"Data has been saved to '{csv_file_path}'")
else:
    # If there's an error, print the status code and error message
    print(f"Error {response.status_code}: {response.text}")
