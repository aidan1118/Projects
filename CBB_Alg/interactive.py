#!/usr/bin/env python3
"""
Interactive College Basketball Prediction System
User-friendly prompt-based interface for all system functionality
"""

import sys
import logging
from utils import setup_logging, ensure_directories
from data_processor import CBBDataProcessor
from config import Config

class InteractiveCBB:
    """Interactive interface for the CBB prediction system"""
    
    def __init__(self):
        # Setup logging (quieter for interactive mode)
        logger = setup_logging('WARNING')
        ensure_directories()
        
        try:
            self.processor = CBBDataProcessor()
            print("College Basketball Prediction System")
            print("=" * 50)
            print("System initialized successfully!")
        except Exception as e:
            print(f"Error initializing system: {e}")
            print("Please check your .env file and API key.")
            sys.exit(1)
    
    def main_menu(self):
        """Display main menu and handle user choice"""
        while True:
            print("\n" + "="*50)
            print("COLLEGE BASKETBALL PREDICTION SYSTEM")
            print("="*50)
            print("1. Look up teams by name")
            print("2. List all teams") 
            print("3. Get team trends & analysis")
            print("4. Compare two teams (matchup analysis)")
            print("5. Refresh team data from API")
            print("6. Help & Examples")
            print("7. Exit")
            print("="*50)
            
            try:
                choice = input("Enter your choice (1-7): ").strip()
                
                if choice == '1':
                    self.lookup_teams()
                elif choice == '2':
                    self.list_teams()
                elif choice == '3':
                    self.get_team_trends()
                elif choice == '4':
                    self.matchup_analysis()
                elif choice == '5':
                    self.refresh_teams()
                elif choice == '6':
                    self.show_help()
                elif choice == '7':
                    print("\nThanks for using CBB Prediction System!")
                    break
                else:
                    print("Invalid choice. Please enter 1-7.")
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
    
    def lookup_teams(self):
        """Interactive team lookup"""
        print("\nTEAM LOOKUP")
        print("-" * 30)
        print("Search for teams by name, location, or abbreviation")
        print("Examples: 'duke', 'north carolina', 'texas', 'GONZ'")
        
        while True:
            search_term = input("\nEnter search term (or 'back' to return): ").strip()
            
            if search_term.lower() == 'back':
                break
                
            if not search_term:
                print("Please enter a search term.")
                continue
            
            try:
                print(f"\nSearching for '{search_term}'...")
                teams = self.processor.load_teams_data()
                matches = self._find_matching_teams(teams, search_term)
                
                if not matches:
                    print(f"No teams found matching '{search_term}'")
                    print("Try partial names like 'carolina', 'state', 'tech'")
                    continue
                
                self._display_team_matches(matches, search_term)
                
                # Ask if user wants to analyze any of these teams
                if len(matches) == 1:
                    if self._ask_yes_no(f"Analyze {matches[0]['Key']} trends?"):
                        self._analyze_single_team(matches[0]['Key'])
                elif len(matches) > 1:
                    self._offer_team_actions(matches)
                        
            except Exception as e:
                print(f"Error during search: {e}")
    
    def list_teams(self):
        """List all teams with pagination"""
        print("\nALL TEAMS")
        print("-" * 20)
        
        try:
            teams = self.processor.load_teams_data()
            sorted_teams = sorted(teams, key=lambda x: x.get('School', ''))
            
            print(f"Total teams: {len(teams)}")
            
            # Pagination
            per_page = 20
            total_pages = (len(sorted_teams) + per_page - 1) // per_page
            current_page = 1
            
            while True:
                start_idx = (current_page - 1) * per_page
                end_idx = min(start_idx + per_page, len(sorted_teams))
                
                print(f"\nPage {current_page} of {total_pages}")
                print("=" * 80)
                print(f"{'Abbrev':<8} {'School':<35} {'Conference'}")
                print("=" * 80)
                
                for team in sorted_teams[start_idx:end_idx]:
                    abbrev = team.get('Key', 'N/A')
                    school = team.get('School', 'Unknown')[:33]
                    conference = team.get('Conference') or 'Independent'
                    print(f"{abbrev:<8} {school:<35} {conference}")
                
                print("\nNavigation: [n]ext, [p]revious, [s]earch, [b]ack to main menu")
                action = input("Choice: ").strip().lower()
                
                if action == 'n' and current_page < total_pages:
                    current_page += 1
                elif action == 'p' and current_page > 1:
                    current_page -= 1
                elif action == 's':
                    search_term = input("Search teams: ").strip()
                    if search_term:
                        matches = self._find_matching_teams(teams, search_term)
                        if matches:
                            self._display_team_matches(matches, search_term)
                elif action == 'b':
                    break
                else:
                    print("Invalid choice or at page boundary.")
                    
        except Exception as e:
            print(f"Error loading teams: {e}")
    
    def get_team_trends(self):
        """Interactive team trends analysis"""
        print("\nTEAM TRENDS ANALYSIS")
        print("-" * 30)
        
        while True:
            team_input = input("Enter team abbreviation (or 'back'): ").strip().upper()
            
            if team_input.lower() == 'back':
                break
                
            if not team_input:
                print("Please enter a team abbreviation.")
                continue
            
            # Validate team exists
            if not self._validate_team(team_input):
                suggestion = self._suggest_team_search(team_input)
                if suggestion:
                    print(f"Did you mean: {suggestion}")
                continue
            
            self._analyze_single_team(team_input)
            break
    
    def matchup_analysis(self):
        """Interactive matchup analysis with team search"""
        print("\nMATCHUP ANALYSIS")
        print("-" * 25)
        print("Compare two teams head-to-head")
        
        # Get first team
        team1 = self._search_and_select_team("first")
        if not team1:
            return
        
        # Get second team
        team2 = self._search_and_select_team("second", exclude_team=team1)
        if not team2:
            return
        
        # Perform analysis
        try:
            print(f"\nAnalyzing {team1} vs {team2}...")
            analysis = self.processor.get_matchup_analysis(team1, team2)
            
            # Debug: Check what we got back
            if isinstance(analysis, str):
                print(f"API Error: {analysis}")
                return
            elif not isinstance(analysis, dict):
                print(f"Unexpected response type: {type(analysis)}")
                return
            
            self._display_matchup_results(analysis, team1, team2)
            
        except Exception as e:
            print(f"Error analyzing matchup: {e}")
            if hasattr(e, '__traceback__'):
                import traceback
                print("Debug info:")
                traceback.print_exc()
    
    def _search_and_select_team(self, position: str, exclude_team: str = None):
        """Search for and select a team for matchup analysis"""
        print(f"\nSelect {position} team:")
        print("You can:")
        print("1. Search by team name (e.g., 'duke', 'north carolina')")
        print("2. Enter exact abbreviation (e.g., 'DUKE', 'NCAR')")
        
        while True:
            search_input = input(f"\nEnter team name/abbreviation (or 'back'): ").strip()
            
            if search_input.lower() == 'back':
                return None
                
            if not search_input:
                print("Please enter a team name or abbreviation.")
                continue
            
            # First check if it's a valid abbreviation
            if self._validate_team(search_input.upper()):
                selected_team = search_input.upper()
                if exclude_team and selected_team == exclude_team:
                    print(f"Please choose a different team (you already selected {exclude_team})")
                    continue
                
                # Show team info and confirm
                teams = self.processor.load_teams_data()
                team_info = next((t for t in teams if t.get('Key', '').upper() == selected_team), None)
                if team_info:
                    print(f"Selected: {team_info.get('School', 'Unknown')} ({selected_team})")
                return selected_team
            
            # If not valid abbreviation, search by name
            try:
                teams = self.processor.load_teams_data()
                matches = self._find_matching_teams(teams, search_input)
                
                if not matches:
                    print(f"No teams found matching '{search_input}'")
                    print("Try partial names like 'carolina', 'state', 'tech'")
                    continue
                
                # Display matches and let user select
                selected_team = self._select_from_matches(matches, exclude_team)
                if selected_team:
                    return selected_team
                    
            except Exception as e:
                print(f"Error during search: {e}")
    
    def _select_from_matches(self, matches, exclude_team=None):
        """Display team matches and let user select one"""
        if len(matches) == 1:
            team = matches[0]
            team_key = team.get('Key', '')
            if exclude_team and team_key == exclude_team:
                print(f"This is the same team you already selected ({exclude_team})")
                return None
            
            school = team.get('School', 'Unknown')
            if self._ask_yes_no(f"Select {school} ({team_key})?"):
                print(f"Selected: {school} ({team_key})")
                return team_key
            return None
        
        # Multiple matches - show numbered list
        # Sort matches for display but keep original order for selection
        sorted_matches = sorted(matches, key=lambda x: x.get('School', ''))
        
        print(f"\nFound {len(matches)} team(s):")
        print("=" * 80)
        print(f"{'#':<3} {'Abbrev':<8} {'School':<30} {'Team Name':<15} {'Conference'}")
        print("=" * 80)
        
        for i, team in enumerate(sorted_matches, 1):
            abbrev = team.get('Key', 'N/A')
            school = team.get('School', 'Unknown')[:28]
            name = team.get('Name', 'Unknown')[:13]
            conference = (team.get('Conference') or 'Independent')[:20]
            
            print(f"{i:<3} {abbrev:<8} {school:<30} {name:<15} {conference}")
        
        while True:
            try:
                choice = input(f"\nSelect team number (1-{len(sorted_matches)}) or 'back': ").strip()
                
                if choice.lower() == 'back':
                    return None
                
                idx = int(choice) - 1
                if 0 <= idx < len(sorted_matches):
                    selected_team = sorted_matches[idx]
                    team_key = selected_team.get('Key', '')
                    
                    if exclude_team and team_key == exclude_team:
                        print(f"Please choose a different team (you already selected {exclude_team})")
                        continue
                    
                    school = selected_team.get('School', 'Unknown')
                    print(f"Selected: {school} ({team_key})")
                    return team_key
                else:
                    print("Invalid selection. Please try again.")
                    
            except ValueError:
                print("Please enter a valid number or 'back'.")
    
    def refresh_teams(self):
        """Refresh team data from API"""
        print("\nREFRESH TEAM DATA")
        print("-" * 25)
        
        if self._ask_yes_no("Download latest team data from API?"):
            try:
                print("Fetching latest team data...")
                teams = self.processor.load_teams_data(force_refresh=True)
                print(f"Successfully updated {len(teams)} teams!")
                
            except Exception as e:
                print(f"Error refreshing data: {e}")
    
    def show_help(self):
        """Show help and examples"""
        print("\nHELP & EXAMPLES")
        print("=" * 30)
        print("How to use this system:")
        print()
        print("1. TEAM LOOKUP:")
        print("   • Search by school name: 'duke', 'north carolina'")
        print("   • Search by location: 'texas', 'florida'") 
        print("   • Search by abbreviation: 'GONZ', 'UK'")
        print()
        print("2. TEAM TRENDS:")
        print("   • Use exact abbreviations: DUKE, NCAR, GONZ")
        print("   • Shows recent performance and upcoming games")
        print()
        print("3. MATCHUP ANALYSIS:")
        print("   • Compare any two teams head-to-head")
        print("   • Analyzes historical trends and betting data")
        print()
        print("COMMON TEAM ABBREVIATIONS:")
        print("   • Duke: DUKE          • North Carolina: NCAR")
        print("   • Kentucky: UK        • Gonzaga: GONZ") 
        print("   • Kansas: KU          • UCLA: UCLA")
        print("   • Villanova: NOVA     • Michigan: MICH")
        print()
        print("TROUBLESHOOTING:")
        print("   • Team not found? Use option 1 to search")
        print("   • API errors? Check your .env file")
        print("   • Need team list? Use option 2")
        
        input("\nPress Enter to continue...")
    
    # Helper methods
    def _find_matching_teams(self, teams, search_term):
        """Find teams matching search term"""
        search_lower = search_term.lower()
        matches = []
        
        for team in teams:
            school = team.get('School', '').lower()
            name = team.get('Name', '').lower()
            key = team.get('Key', '').lower()
            
            if (search_lower in school or 
                search_lower in name or 
                search_lower in key):
                matches.append(team)
        
        return matches
    
    def _display_team_matches(self, matches, search_term):
        """Display team search results"""
        print(f"\nFound {len(matches)} team(s) matching '{search_term}':")
        print("=" * 80)
        print(f"{'#':<3} {'Abbrev':<8} {'School':<30} {'Team Name':<15} {'Conference'}")
        print("=" * 80)
        
        for i, team in enumerate(sorted(matches, key=lambda x: x.get('School', '')), 1):
            abbrev = team.get('Key', 'N/A')
            school = team.get('School', 'Unknown')[:28]
            name = team.get('Name', 'Unknown')[:13]
            conference = (team.get('Conference') or 'Independent')[:20]
            
            print(f"{i:<3} {abbrev:<8} {school:<30} {name:<15} {conference}")
    
    def _offer_team_actions(self, matches):
        """Offer actions for multiple team matches"""
        # Sort matches to match the display order
        sorted_matches = sorted(matches, key=lambda x: x.get('School', ''))
        
        print(f"\nActions:")
        print("1. Analyze trends for a team")
        print("2. Continue searching")
        
        choice = input("Choice (1-2): ").strip()
        
        if choice == '1':
            team_num = input(f"Enter team number (1-{len(sorted_matches)}): ").strip()
            try:
                idx = int(team_num) - 1
                if 0 <= idx < len(sorted_matches):
                    self._analyze_single_team(sorted_matches[idx]['Key'])
            except ValueError:
                print("Invalid team number.")
    
    def _analyze_single_team(self, team_abbrev):
        """Analyze trends for a single team"""
        try:
            print(f"\nAnalyzing {team_abbrev}...")
            trends_data = self.processor.get_team_trends(team_abbrev)
            self._display_team_trends(trends_data, team_abbrev)
            
        except Exception as e:
            print(f"Error analyzing {team_abbrev}: {e}")
    
    def _display_team_trends(self, trends_data, team_abbrev):
        """Display team trends in a user-friendly format"""
        print(f"\nTRENDS ANALYSIS: {team_abbrev}")
        print("=" * 50)
        
        if not trends_data:
            print("No trends data available")
            return
        
        # Handle both single object and list responses
        if isinstance(trends_data, dict):
            trends_list = [trends_data]
        else:
            trends_list = trends_data
        
        for trend in trends_list:
            team_name = trend.get('Team', 'Unknown')
            print(f"Team: {team_name}")
            
            # Show data source info
            data_source = trend.get('_data_source', 'unknown')
            if data_source == 'betting_trends':
                print("Using betting data (stats unavailable)")
            elif data_source in ['games_data', 'season_statistics', 'game_statistics']:
                print("Using actual game statistics")
            
            # Show upcoming game if available
            if 'UpcomingGame' in trend:
                upcoming = trend.get('UpcomingGame', {})
                home_team = upcoming.get('HomeTeam', 'TBD')
                away_team = upcoming.get('AwayTeam', 'TBD')
                print(f"Next Game: {away_team} @ {home_team}")
            
            # Show recent trends - always check for TeamGameTrends
            team_trends = trend.get('TeamGameTrends', [])
            if team_trends:
                print(f"\nRecent Performance:")
                print("-" * 40)
                
                for game_trend in team_trends[:8]:  # Show top 8 trends
                    scope = game_trend.get('Scope', 'Unknown')
                    wins = game_trend.get('Wins', 0)
                    losses = game_trend.get('Losses', 0)
                    avg_score = game_trend.get('AverageScore', 0)
                    avg_opp_score = game_trend.get('AverageOpponentScore', 0)
                    
                    # Calculate total games from wins + losses
                    total_games = wins + losses
                    
                    print(f"  {scope:<25}: {wins}-{losses} (avg: {avg_score:.1f}, opp: {avg_opp_score:.1f})")
            else:
                print("No detailed trends available")
            
            # Show detailed statistics if available
            detailed_stats = trend.get('DetailedStats', {})
            if detailed_stats:
                print(f"\nDetailed Statistics:")
                print("-" * 40)
                
                # Shooting stats
                shooting = detailed_stats.get('Shooting', {})
                if shooting:
                    print("Shooting:")
                    for stat_name, stat_value in shooting.items():
                        print(f"  {stat_name:<15}: {stat_value}")
                
                # Per game stats
                per_game = detailed_stats.get('PerGame', {})
                if per_game:
                    print("\nPer Game Averages:")
                    for stat_name, stat_value in per_game.items():
                        print(f"  {stat_name:<12}: {stat_value}")
        
        print(f"\nFull report saved as PDF in data/ directory")
    
    def _display_matchup_results(self, analysis, team1, team2):
        """Display comprehensive matchup analysis results"""
        print(f"\nMATCHUP ANALYSIS: {team1} vs {team2}")
        print("=" * 70)
        
        # Check if analysis is valid dictionary
        if not isinstance(analysis, dict):
            print(f"Unable to analyze matchup: {analysis}")
            return
        
        matchup_info = analysis.get('matchup_info', {})
        team1_info = matchup_info.get('team1', {})
        team2_info = matchup_info.get('team2', {})
        
        print(f"{team1_info.get('School', team1)} ({team1}) vs {team2_info.get('School', team2)} ({team2})")
        print(f"Analysis Date: {matchup_info.get('analysis_date', 'Unknown')}")
        
        # Get the full matchup data for detailed display
        matchup_data = analysis.get('_raw_matchup_data', {})
        team_trends_data = matchup_data.get('TeamTrends', [])
        matchup_trends_data = matchup_data.get('TeamMatchupTrends', [])
        opponent_matchup_trends = matchup_data.get('OpponentMatchupTrends', [])
        previous_games = matchup_data.get('PreviousGames', [])
        
        # Display detailed team performance
        print(f"\nDETAILED TEAM PERFORMANCE")
        print("=" * 70)
        
        for team_data in team_trends_data:
            team_key = team_data.get('Team', '')
            school_name = team1_info.get('School', team1) if team_key == team1 else team2_info.get('School', team2)
            
            print(f"\n{school_name} ({team_key})")
            print("-" * 40)
            
            # Upcoming game
            upcoming = team_data.get('UpcomingGame', {})
            if upcoming:
                away = upcoming.get('AwayTeam', 'TBD')
                home = upcoming.get('HomeTeam', 'TBD')
                date = upcoming.get('DateTime', 'TBD')[:10] if upcoming.get('DateTime') else 'TBD'
                channel = upcoming.get('Channel', 'TBD')
                print(f"Next Game: {away} @ {home} on {date} ({channel})")
            
            # Team game trends
            game_trends = team_data.get('TeamGameTrends', [])
            if game_trends:
                print(f"\nRecent Performance:")
                for trend in game_trends[:6]:  # Show top 6 trends
                    scope = trend.get('Scope', '')
                    wins = trend.get('Wins', 0)
                    losses = trend.get('Losses', 0)
                    avg_score = trend.get('AverageScore', 0)
                    avg_opp = trend.get('AverageOpponentScore', 0)
                    print(f"  {scope:<20}: {wins}-{losses} | Avg: {avg_score:.1f}-{avg_opp:.1f}")
        
        # Head-to-head matchup trends
        if matchup_trends_data or opponent_matchup_trends:
            print(f"\nHEAD-TO-HEAD TRENDS")
            print("=" * 70)
            
            # Show matchup trends for team1
            team1_matchups = [t for t in matchup_trends_data if t.get('Team') == team1]
            if team1_matchups:
                print(f"\n{team1} vs {team2} Performance:")
                for trend in team1_matchups[:5]:
                    scope = trend.get('Scope', '')
                    wins = trend.get('Wins', 0)
                    losses = trend.get('Losses', 0)
                    avg_score = trend.get('AverageScore', 0)
                    avg_opp = trend.get('AverageOpponentScore', 0)
                    print(f"  {scope:<20}: {wins}-{losses} | Avg: {avg_score:.1f}-{avg_opp:.1f}")
            
            # Show matchup trends for team2
            team2_matchups = [t for t in opponent_matchup_trends if t.get('Team') == team2]
            if team2_matchups:
                print(f"\n{team2} vs {team1} Performance:")
                for trend in team2_matchups[:5]:
                    scope = trend.get('Scope', '')
                    wins = trend.get('Wins', 0)
                    losses = trend.get('Losses', 0)
                    avg_score = trend.get('AverageScore', 0)
                    avg_opp = trend.get('AverageOpponentScore', 0)
                    print(f"  {scope:<20}: {wins}-{losses} | Avg: {avg_score:.1f}-{avg_opp:.1f}")
        
        # Previous games history
        if previous_games:
            print(f"\nRECENT HEAD-TO-HEAD GAMES")
            print("=" * 70)
            for game in previous_games[:5]:  # Show last 5 games
                date = game.get('DateTime', '')[:10] if game.get('DateTime') else 'Unknown'
                away_team = game.get('AwayTeam', '')
                home_team = game.get('HomeTeam', '')
                away_score = game.get('AwayTeamScore', 0)
                home_score = game.get('HomeTeamScore', 0)
                
                winner = home_team if home_score > away_score else away_team
                print(f"  {date}: {away_team} {away_score} - {home_score} {home_team} (Winner: {winner})")
        
        # Betting analysis and key factors
        betting_analysis = analysis.get('betting_analysis', {})
        if betting_analysis.get('key_factors'):
            print(f"\nKEY BETTING FACTORS")
            print("=" * 70)
            for factor in betting_analysis['key_factors']:
                print(f"• {factor}")
        
        print(f"\nDetailed analysis saved as PDF in data/ directory")
    
    def _validate_team(self, team_abbrev):
        """Validate if team abbreviation exists"""
        try:
            teams = self.processor.load_teams_data()
            return any(team.get('Key', '').upper() == team_abbrev.upper() for team in teams)
        except:
            return False
    
    def _suggest_team_search(self, team_input):
        """Suggest using search for invalid team"""
        return f"python main.py --lookup {team_input.lower()}"
    
    def _ask_yes_no(self, question):
        """Ask a yes/no question"""
        while True:
            answer = input(f"{question} (y/n): ").strip().lower()
            if answer in ['y', 'yes']:
                return True
            elif answer in ['n', 'no']:
                return False
            else:
                print("Please answer 'y' or 'n'")

def main():
    """Run the interactive CBB system"""
    try:
        app = InteractiveCBB()
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())