#!/usr/bin/env python3
"""
College Basketball Prediction System
Main CLI interface for analyzing college basketball matchups and trends
"""

import argparse
import sys
import logging
from typing import Optional

from utils import setup_logging, ensure_directories
from data_processor import CBBDataProcessor
from config import Config

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='College Basketball Prediction System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --list-teams                    # List all teams
  python main.py --lookup "north carolina"      # Find North Carolina teams
  python main.py --lookup duke                  # Find Duke
  python main.py --team-trends DUKE             # Get trends for Duke
  python main.py --matchup DUKE NCAR            # Analyze Duke vs UNC matchup
  python main.py --matchup GONZAGA BAYLOR -v    # Verbose analysis
        """
    )
    
    # Commands
    parser.add_argument('--list-teams', action='store_true',
                       help='List all available teams')
    
    parser.add_argument('--team-trends', metavar='TEAM',
                       help='Get trends for a specific team (use team abbreviation)')
    
    parser.add_argument('--matchup', nargs=2, metavar=('TEAM1', 'TEAM2'),
                       help='Analyze matchup between two teams')
    
    parser.add_argument('--lookup', metavar='SEARCH_TERM',
                       help='Search for teams by name and show their abbreviations')
    
    parser.add_argument('--refresh-teams', action='store_true',
                       help='Force refresh of teams data from API')
    
    # Options
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Set logging level')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(args.log_level)
    ensure_directories()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # Initialize data processor
        processor = CBBDataProcessor()
        
        # Handle different commands
        if args.list_teams:
            list_teams(processor, args.refresh_teams)
        
        elif args.team_trends:
            get_team_trends(processor, args.team_trends)
        
        elif args.matchup:
            analyze_matchup(processor, args.matchup[0], args.matchup[1])
        
        elif args.lookup:
            lookup_teams(processor, args.lookup)
        
        else:
            parser.print_help()
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            logger.exception("Full error details:")
        return 1

def list_teams(processor: CBBDataProcessor, refresh: bool = False):
    """List all available teams"""
    print("Loading teams data...")
    teams = processor.load_teams_data(force_refresh=refresh)
    
    print(f"\nFound {len(teams)} teams:")
    print("=" * 60)
    print(f"{'Abbrev':<8} {'School':<40} {'Conference'}")
    print("=" * 60)
    
    for team in sorted(teams, key=lambda x: x.get('School', '')):
        abbrev = team.get('Key', 'N/A')
        school = team.get('School', 'Unknown')[:38]
        conference = team.get('Conference', 'N/A')
        print(f"{abbrev:<8} {school:<40} {conference}")

def get_team_trends(processor: CBBDataProcessor, team: str):
    """Get and display trends for a specific team"""
    try:
        print(f"Fetching trends for {team}...")
        trends_data = processor.get_team_trends(team)
        
        print(f"\nTrends Analysis for {team.upper()}")
        print("=" * 50)
        
        if not trends_data:
            print("No trends data available")
            return
        
        # Handle both single object and list responses
        if isinstance(trends_data, dict):
            trends_list = [trends_data]
        else:
            trends_list = trends_data
        
        # Display key metrics
        for trend in trends_list:
            team_name = trend.get('Team', 'Unknown')
            print(f"\nTeam: {team_name}")
            
            # Check if this is the main team data structure
            if 'UpcomingGame' in trend:
                upcoming = trend.get('UpcomingGame', {})
                print(f"Next Game: {upcoming.get('AwayTeam', 'TBD')} @ {upcoming.get('HomeTeam', 'TBD')}")
                
                # Look for trend statistics in TeamGameTrends
                team_trends = trend.get('TeamGameTrends', [])
                if team_trends:
                    print(f"Recent Trends ({len(team_trends)} entries):")
                    for i, game_trend in enumerate(team_trends[:5]):  # Show first 5
                        scope = game_trend.get('Scope', 'Unknown')
                        games = game_trend.get('Games', 'N/A')
                        wins = game_trend.get('Wins', 'N/A')
                        print(f"  {scope}: {wins}-{games-wins if isinstance(games, int) and isinstance(wins, int) else 'N/A'}")
                else:
                    print("No detailed trends available")
            else:
                # Fallback to original format
                wins = trend.get('Wins', 'N/A')
                losses = trend.get('Losses', 'N/A') 
                win_pct = trend.get('Percentage', 'N/A')
                
                print(f"Record: {wins}-{losses} ({win_pct})")
                
                avg_score = trend.get('AverageScore', 'N/A')
                avg_opp_score = trend.get('AverageOpponentScore', 'N/A')
                
                print(f"Average Score: {avg_score}")
                print(f"Average Opponent Score: {avg_opp_score}")
        
        print(f"\nDetailed data saved to data/ directory")
        
    except Exception as e:
        print(f"Error getting trends for {team}: {e}")

def lookup_teams(processor: CBBDataProcessor, search_term: str):
    """Search for teams by name and display their abbreviations"""
    try:
        print(f"Searching for teams matching '{search_term}'...")
        teams = processor.load_teams_data()
        
        # Search for teams matching the search term (case insensitive)
        search_lower = search_term.lower()
        matches = []
        
        for team in teams:
            school = team.get('School', '').lower()
            name = team.get('Name', '').lower()
            key = team.get('Key', '').lower()
            
            # Check if search term appears in school name, team name, or abbreviation
            if (search_lower in school or 
                search_lower in name or 
                search_lower in key):
                matches.append(team)
        
        if not matches:
            print(f"No teams found matching '{search_term}'")
            print("\nTip: Try searching with partial names like 'carolina', 'state', 'tech', etc.")
            return
        
        # Display results
        print(f"\nFound {len(matches)} team(s) matching '{search_term}':")
        print("=" * 80)
        print(f"{'Abbrev':<8} {'School':<35} {'Team Name':<20} {'Conference'}")
        print("=" * 80)
        
        for team in sorted(matches, key=lambda x: x.get('School', '')):
            abbrev = team.get('Key', 'N/A')
            school = team.get('School', 'Unknown')[:33]
            name = team.get('Name', 'Unknown')[:18]
            conference = team.get('Conference') or 'Independent'
            
            print(f"{abbrev:<8} {school:<35} {name:<20} {conference}")
        
        # Show usage example if results found
        if matches:
            first_team = matches[0].get('Key', 'TEAM')
            print(f"\nUsage examples:")
            print(f"  python main.py --team-trends {first_team}")
            if len(matches) > 1:
                second_team = matches[1].get('Key', 'TEAM2')
                print(f"  python main.py --matchup {first_team} {second_team}")
        
    except Exception as e:
        print(f"Error searching for teams: {e}")

def analyze_matchup(processor: CBBDataProcessor, team1: str, team2: str):
    """Analyze matchup between two teams"""
    try:
        print(f"Analyzing matchup: {team1.upper()} vs {team2.upper()}")
        analysis = processor.get_matchup_analysis(team1, team2)
        
        # Display matchup info
        matchup_info = analysis.get('matchup_info', {})
        team1_info = matchup_info.get('team1', {})
        team2_info = matchup_info.get('team2', {})
        
        print("\n" + "="*60)
        print("MATCHUP ANALYSIS")
        print("="*60)
        
        print(f"\n{team1_info.get('School', team1)} ({team1_info.get('Key', team1)})")
        print(f"vs")
        print(f"{team2_info.get('School', team2)} ({team2_info.get('Key', team2)})")
        
        # Display trends summary
        trends = analysis.get('trends', {})
        if trends:
            print(f"\n{'Team':<20} {'Record':<12} {'Avg Score':<10} {'Avg Opp':<10}")
            print("-" * 52)
            
            for team_key, team_trends in trends.items():
                overall = team_trends.get('overall', {})
                wins = overall.get('wins', 'N/A')
                losses = overall.get('losses', 'N/A')
                record = f"{wins}-{losses}"
                avg_score = f"{overall.get('average_score', 0):.1f}"
                avg_opp = f"{overall.get('average_opponent_score', 0):.1f}"
                
                print(f"{team_key:<20} {record:<12} {avg_score:<10} {avg_opp:<10}")
        
        # Display betting analysis
        betting_analysis = analysis.get('betting_analysis', {})
        if betting_analysis.get('key_factors'):
            print(f"\nKEY FACTORS:")
            for factor in betting_analysis['key_factors']:
                print(f"• {factor}")
        
        print(f"\nDetailed analysis saved to data/ directory")
        
    except Exception as e:
        print(f"Error analyzing matchup {team1} vs {team2}: {e}")

if __name__ == '__main__':
    sys.exit(main())