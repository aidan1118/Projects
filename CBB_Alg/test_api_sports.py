#!/usr/bin/env python3
"""
Test script for API-Sports Basketball API
https://v1.basketball.api-sports.io
"""
import requests
import json

def test_api_sports():
    """Test the API-Sports basketball API"""
    
    api_key = "cd1959e3625c3770d09260fbe601741f"
    base_url = "https://v1.basketball.api-sports.io"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "v1.basketball.api-sports.io"
    }
    
    print("Testing API-Sports Basketball API")
    print("=" * 50)
    
    # Test 1: Get leagues to see what's available
    print("1. Testing leagues endpoint...")
    try:
        response = requests.get(f"{base_url}/leagues", headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response structure: {list(data.keys())}")
            
            # Look for college basketball leagues
            leagues = data.get('response', [])
            print(f"\nFound {len(leagues)} leagues")
            
            college_leagues = [l for l in leagues if 'college' in l.get('name', '').lower() or 
                              'ncaa' in l.get('name', '').lower() or
                              l.get('id') == 116]
            
            if college_leagues:
                print(f"\nCollege basketball leagues found:")
                for league in college_leagues[:10]:  # Show first 10
                    print(f"  ID: {league.get('id')} - {league.get('name')} ({league.get('type')})")
            else:
                print("\nNo obvious college leagues found. Showing first 10 leagues:")
                for league in leagues[:10]:
                    print(f"  ID: {league.get('id')} - {league.get('name')} ({league.get('type')})")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Leagues test failed: {e}")
    
    # Test 2: Try to get seasons for league 116 (mens college basketball)
    print("\n" + "=" * 50)
    print("2. Testing seasons for league 116...")
    try:
        response = requests.get(f"{base_url}/seasons", headers=headers, params={"league": 116}, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            seasons = data.get('response', [])
            print(f"Available seasons: {seasons}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Seasons test failed: {e}")
    
    # Test 2b: Try seasons without league parameter
    print("\n2b. Testing all seasons...")
    try:
        response = requests.get(f"{base_url}/seasons", headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            seasons = data.get('response', [])
            print(f"All available seasons: {seasons[:10]}")  # Show first 10
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"All seasons test failed: {e}")
    
    # Test 3: Try to get teams for college basketball with different season formats
    print("\n" + "=" * 50)  
    print("3. Testing teams for league 116...")
    
    season_formats = ["2024-25", "2024", "2023-24", "2023"]
    for season in season_formats:
        print(f"\n3.{season_formats.index(season)+1} Trying season: {season}")
        try:
            response = requests.get(f"{base_url}/teams", headers=headers, 
                                   params={"league": 116, "season": season}, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                teams = data.get('response', [])
                print(f"Found {len(teams)} teams for {season}")
                
                if teams:
                    # Look for Duke
                    duke_teams = [t for t in teams if 'duke' in t.get('name', '').lower()]
                    if duke_teams:
                        print(f"\nDuke teams found:")
                        for team in duke_teams:
                            print(f"  ID: {team.get('id')} - {team.get('name')}")
                    
                    # Show first 5 teams
                    print(f"\nFirst 5 teams:")
                    for team in teams[:5]:
                        print(f"  ID: {team.get('id')} - {team.get('name')}")
                    break  # Found data, stop trying other seasons
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Teams test failed for {season}: {e}")
    
    # Test 3b: Try teams without league parameter to see what's available
    print(f"\n3b. Testing teams without league filter...")
    try:
        response = requests.get(f"{base_url}/teams", headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            teams = data.get('response', [])
            print(f"Found {len(teams)} total teams")
            
            # Look for any basketball teams
            basketball_teams = [t for t in teams[:50] if 'basketball' in str(t).lower() or 'college' in str(t).lower()]
            if basketball_teams:
                print(f"Found {len(basketball_teams)} basketball/college teams in first 50:")
                for team in basketball_teams[:5]:
                    print(f"  ID: {team.get('id')} - {team.get('name')}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"All teams test failed: {e}")
    
    # Test 4: Try to get games
    print("\n" + "=" * 50)
    print("4. Testing games endpoint...")
    try:
        response = requests.get(f"{base_url}/games", headers=headers,
                               params={"league": 116, "season": "2023-24"}, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            games = data.get('response', [])
            print(f"Found {len(games)} games")
            
            if games:
                # Show first game structure
                print(f"\nFirst game structure:")
                game = games[0]
                for key, value in game.items():
                    if isinstance(value, dict):
                        print(f"  {key}: {list(value.keys())}")
                    else:
                        print(f"  {key}: {value}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Games test failed: {e}")
    
    # Test 5: Check API status/quota
    print("\n" + "=" * 50)
    print("5. Testing API status...")
    try:
        response = requests.get(f"{base_url}/status", headers=headers, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"API Status: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Status test failed: {e}")

if __name__ == "__main__":
    test_api_sports()