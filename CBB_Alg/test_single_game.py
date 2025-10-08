#!/usr/bin/env python3
"""
Test script to check single game data from the API
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import SportsDataAPIClient
from config import Config
import json

def test_single_game():
    """Test getting a single game to see the actual score format"""
    
    # Initialize API client
    api_client = SportsDataAPIClient()
    
    print("Testing single game data...")
    print("=" * 50)
    
    try:
        # First try to get season stats to see what data is available
        print("Getting Duke season stats with both API keys...")
        
        # Try with stats API key
        try:
            season_stats = api_client.get_team_stats('2025')
            duke_stats = next((s for s in season_stats if s.get('Team') == 'DUKE'), None)
            
            if duke_stats:
                print("\n--- Duke Season Stats (Stats API Key) ---")
                for key, value in duke_stats.items():
                    print(f"{key}: {value}")
            else:
                print("No Duke stats with stats API key")
        except Exception as e:
            print(f"Stats API key failed: {e}")
        
        # Try games endpoint with both API keys
        print("\nTrying games endpoint with original API key...")
        try:
            games_data = api_client.get_games('2025')
            
            if games_data and len(games_data) > 0:
                # Find a Duke game
                duke_games = [g for g in games_data if g.get('HomeTeam') == 'DUKE' or g.get('AwayTeam') == 'DUKE']
                
                if duke_games:
                    print(f"\nFound {len(duke_games)} Duke games")
                    
                    # Show first few Duke games
                    for i, game in enumerate(duke_games[:3]):
                        print(f"\n--- Duke Game {i+1} ---")
                        print(f"Date: {game.get('DateTime', 'N/A')}")
                        print(f"Home: {game.get('HomeTeam', 'N/A')} - Score: {game.get('HomeScore', 'N/A')}")
                        print(f"Away: {game.get('AwayTeam', 'N/A')} - Score: {game.get('AwayScore', 'N/A')}")
                        print(f"Status: {game.get('Status', 'N/A')}")
                        
                        # Show all available fields for first game
                        if i == 0:
                            print("\n--- All fields in first game ---")
                            for key, value in game.items():
                                print(f"{key}: {value}")
                else:
                    print("No Duke games found")
                    
                    # Show sample game from any team
                    print("\n--- Sample game from any team ---")
                    sample_game = games_data[0]
                    for key, value in sample_game.items():
                        print(f"{key}: {value}")
            else:
                print("No games data returned")
        except Exception as e:
            print(f"Games endpoint with original key failed: {e}")
        
        # Try games endpoint with stats API key
        print("\nTrying games endpoint with stats API key...")
        try:
            # Manually test with stats API key
            import requests
            stats_key = api_client.stats_api_key
            if stats_key:
                url = f"https://api.sportsdata.io/v3/cbb/scores/json/Games/2025?key={stats_key}"
                response = requests.get(url, timeout=30)
                print(f"Stats key response status: {response.status_code}")
                
                if response.status_code == 200:
                    games_data = response.json()
                    duke_games = [g for g in games_data if g.get('HomeTeam') == 'DUKE' or g.get('AwayTeam') == 'DUKE']
                    
                    if duke_games:
                        print(f"\n🎉 SUCCESS! Found {len(duke_games)} Duke games with stats API key")
                        
                        # Show first Duke game with all fields
                        game = duke_games[0]
                        print(f"\n--- Sample Duke Game (All Fields) ---")
                        for key, value in game.items():
                            print(f"{key}: {value}")
                        
                        # Show a few more games to see if scores appear
                        print(f"\n--- Next 5 Duke Games ---")
                        for i, game in enumerate(duke_games[1:6], 2):
                            print(f"\nGame {i}:")
                            print(f"Date: {game.get('DateTime', 'N/A')}")
                            print(f"Home: {game.get('HomeTeam', 'N/A')}")
                            print(f"Away: {game.get('AwayTeam', 'N/A')}")
                            print(f"Status: {game.get('Status', 'N/A')}")
                            
                            # Look for any score-related fields
                            score_fields = [k for k in game.keys() if 'score' in k.lower() or 'point' in k.lower()]
                            if score_fields:
                                print("Score fields found:")
                                for field in score_fields:
                                    print(f"  {field}: {game.get(field)}")
                    else:
                        print("No Duke games found with stats key")
                else:
                    print(f"Stats key also failed: {response.status_code} - {response.text}")
            else:
                print("No stats API key available")
        except Exception as e:
            print(f"Stats API key test failed: {e}")
        
        # Try different season formats
        print("\n" + "=" * 50)
        print("Trying different season formats...")
        
        for season in ['2025', '2024', '2023']:
            try:
                print(f"\nTrying season {season}...")
                season_stats = api_client.get_team_stats(season)
                duke_stats = next((s for s in season_stats if s.get('Team') == 'DUKE'), None)
                
                if duke_stats:
                    print(f"--- Duke Stats for {season} Season ---")
                    games = duke_stats.get('Games', 0)
                    points = duke_stats.get('Points', 0)
                    print(f"Games: {games}")
                    print(f"Total Points: {points}")
                    print(f"Calculated Average: {points/games if games > 0 else 0:.1f}")
                    print(f"Wins: {duke_stats.get('Wins', 0)}")
                    print(f"Losses: {duke_stats.get('Losses', 0)}")
                    break
            except Exception as e:
                print(f"Season {season} failed: {e}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_single_game()