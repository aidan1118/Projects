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
            print("🏀 College Basketball Prediction System")
            print("=" * 50)
            print("System initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing system: {e}")
            print("Please check your .env file and API key.")
            sys.exit(1)
    
    def main_menu(self):
        """Display main menu and handle user choice"""
        while True:
            print("\n" + "="*50)
            print("🏀 COLLEGE BASKETBALL PREDICTION SYSTEM")
            print("="*50)
            print("1. 🔍 Look up teams by name")
            print("2. 📋 List all teams") 
            print("3. 📊 Get team trends & analysis")
            print("4. ⚔️  Compare two teams (matchup analysis)")
            print("5. 🔄 Refresh team data from API")
            print("6. ❓ Help & Examples")
            print("7. 🚪 Exit")
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
                    print("\n👋 Thanks for using CBB Prediction System!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-7.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
    
    def lookup_teams(self):
        """Interactive team lookup"""
        print("\n🔍 TEAM LOOKUP")
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
                    print(f"❌ No teams found matching '{search_term}'")
                    print("💡 Try partial names like 'carolina', 'state', 'tech'")
                    continue
                
                self._display_team_matches(matches, search_term)
                
                # Ask if user wants to analyze any of these teams
                if len(matches) == 1:
                    if self._ask_yes_no(f"Analyze {matches[0]['Key']} trends?"):
                        self._analyze_single_team(matches[0]['Key'])
                elif len(matches) > 1:
                    self._offer_team_actions(matches)
                        
            except Exception as e:
                print(f"❌ Error during search: {e}")
    
    def list_teams(self):
        """List all teams with pagination"""
        print("\n📋 ALL TEAMS")
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
                
                print(f"\n📄 Page {current_page} of {total_pages}")
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
            print(f"❌ Error loading teams: {e}")
    
    def get_team_trends(self):
        """Interactive team trends analysis"""
        print("\n📊 TEAM TRENDS ANALYSIS")
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
                    print(f"💡 Did you mean: {suggestion}")
                continue
            
            self._analyze_single_team(team_input)
            break
    
    def matchup_analysis(self):
        """Interactive matchup analysis"""
        print("\n⚔️  MATCHUP ANALYSIS")
        print("-" * 25)
        print("Compare two teams head-to-head")
        
        team1 = None
        team2 = None
        
        # Get first team
        while not team1:
            team1_input = input("Enter first team abbreviation (or 'back'): ").strip().upper()
            
            if team1_input.lower() == 'back':
                return
                
            if self._validate_team(team1_input):
                team1 = team1_input
            else:
                suggestion = self._suggest_team_search(team1_input)
                if suggestion:
                    print(f"💡 Try searching: python main.py --lookup {team1_input.lower()}")
        
        # Get second team
        while not team2:
            team2_input = input("Enter second team abbreviation (or 'back'): ").strip().upper()
            
            if team2_input.lower() == 'back':
                return
                
            if team2_input == team1:
                print("Please choose a different team for comparison.")
                continue
                
            if self._validate_team(team2_input):
                team2 = team2_input
            else:
                suggestion = self._suggest_team_search(team2_input)
                if suggestion:
                    print(f"💡 Try searching: python main.py --lookup {team2_input.lower()}")
        
        # Perform analysis
        try:
            print(f"\n🔍 Analyzing {team1} vs {team2}...")
            analysis = self.processor.get_matchup_analysis(team1, team2)
            self._display_matchup_results(analysis, team1, team2)
            
        except Exception as e:
            print(f"❌ Error analyzing matchup: {e}")
    
    def refresh_teams(self):
        """Refresh team data from API"""
        print("\n🔄 REFRESH TEAM DATA")
        print("-" * 25)
        
        if self._ask_yes_no("Download latest team data from API?"):
            try:
                print("📡 Fetching latest team data...")
                teams = self.processor.load_teams_data(force_refresh=True)
                print(f"✅ Successfully updated {len(teams)} teams!")
                
            except Exception as e:
                print(f"❌ Error refreshing data: {e}")
    
    def show_help(self):
        """Show help and examples"""
        print("\n❓ HELP & EXAMPLES")
        print("=" * 30)
        print("📋 How to use this system:")
        print()
        print("1. 🔍 TEAM LOOKUP:")
        print("   • Search by school name: 'duke', 'north carolina'")
        print("   • Search by location: 'texas', 'florida'") 
        print("   • Search by abbreviation: 'GONZ', 'UK'")
        print()
        print("2. 📊 TEAM TRENDS:")
        print("   • Use exact abbreviations: DUKE, NCAR, GONZ")
        print("   • Shows recent performance and upcoming games")
        print()
        print("3. ⚔️  MATCHUP ANALYSIS:")
        print("   • Compare any two teams head-to-head")
        print("   • Analyzes historical trends and betting data")
        print()
        print("💡 COMMON TEAM ABBREVIATIONS:")
        print("   • Duke: DUKE          • North Carolina: NCAR")
        print("   • Kentucky: UK        • Gonzaga: GONZ") 
        print("   • Kansas: KU          • UCLA: UCLA")
        print("   • Villanova: NOVA     • Michigan: MICH")
        print()
        print("🔧 TROUBLESHOOTING:")
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
        print(f"\n✅ Found {len(matches)} team(s) matching '{search_term}':")
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
        print(f"\n🎯 Actions:")
        print("1. Analyze trends for a team")
        print("2. Compare two teams")
        print("3. Continue searching")
        
        choice = input("Choice (1-3): ").strip()
        
        if choice == '1':
            team_num = input(f"Enter team number (1-{len(matches)}): ").strip()
            try:
                idx = int(team_num) - 1
                if 0 <= idx < len(matches):
                    self._analyze_single_team(matches[idx]['Key'])
            except ValueError:
                print("Invalid team number.")
        
        elif choice == '2':
            print("Select two teams to compare:")
            team1_num = input(f"First team number (1-{len(matches)}): ").strip()
            team2_num = input(f"Second team number (1-{len(matches)}): ").strip()
            
            try:
                idx1 = int(team1_num) - 1
                idx2 = int(team2_num) - 1
                
                if (0 <= idx1 < len(matches) and 0 <= idx2 < len(matches) and idx1 != idx2):
                    team1 = matches[idx1]['Key']
                    team2 = matches[idx2]['Key']
                    analysis = self.processor.get_matchup_analysis(team1, team2)
                    self._display_matchup_results(analysis, team1, team2)
                else:
                    print("Invalid team numbers or same team selected.")
            except (ValueError, Exception) as e:
                print(f"Error: {e}")
    
    def _analyze_single_team(self, team_abbrev):
        """Analyze trends for a single team"""
        try:
            print(f"\n📊 Analyzing {team_abbrev}...")
            trends_data = self.processor.get_team_trends(team_abbrev)
            self._display_team_trends(trends_data, team_abbrev)
            
        except Exception as e:
            print(f"❌ Error analyzing {team_abbrev}: {e}")
    
    def _display_team_trends(self, trends_data, team_abbrev):
        """Display team trends in a user-friendly format"""
        print(f"\n📊 TRENDS ANALYSIS: {team_abbrev}")
        print("=" * 50)
        
        if not trends_data:
            print("❌ No trends data available")
            return
        
        # Handle both single object and list responses
        if isinstance(trends_data, dict):
            trends_list = [trends_data]
        else:
            trends_list = trends_data
        
        for trend in trends_list:
            team_name = trend.get('Team', 'Unknown')
            print(f"🏀 Team: {team_name}")
            
            # Show upcoming game
            if 'UpcomingGame' in trend:
                upcoming = trend.get('UpcomingGame', {})
                home_team = upcoming.get('HomeTeam', 'TBD')
                away_team = upcoming.get('AwayTeam', 'TBD')
                print(f"🆚 Next Game: {away_team} @ {home_team}")
                
                # Show recent trends
                team_trends = trend.get('TeamGameTrends', [])
                if team_trends:
                    print(f"\n📈 Recent Performance:")
                    print("-" * 40)
                    
                    for game_trend in team_trends[:8]:  # Show top 8 trends
                        scope = game_trend.get('Scope', 'Unknown')
                        games = game_trend.get('Games', 0)
                        wins = game_trend.get('Wins', 0)
                        losses = games - wins if isinstance(games, int) and isinstance(wins, int) else 'N/A'
                        avg_score = game_trend.get('AverageScore', 0)
                        
                        print(f"  {scope:<25}: {wins}-{losses} (avg: {avg_score:.1f})")
                else:
                    print("📊 No detailed trends available")
        
        print(f"\n💾 Full data saved to data/ directory")
    
    def _display_matchup_results(self, analysis, team1, team2):
        """Display matchup analysis results"""
        print(f"\n⚔️  MATCHUP: {team1} vs {team2}")
        print("=" * 50)
        
        matchup_info = analysis.get('matchup_info', {})
        team1_info = matchup_info.get('team1', {})
        team2_info = matchup_info.get('team2', {})
        
        print(f"🏀 {team1_info.get('School', team1)} ({team1})")
        print(f"   vs")
        print(f"🏀 {team2_info.get('School', team2)} ({team2})")
        
        trends = analysis.get('trends', {})
        if trends:
            print(f"\n📊 TEAM COMPARISON:")
            print("-" * 50)
            
            for team_key, team_trends in trends.items():
                overall = team_trends.get('overall', {})
                wins = overall.get('wins', 0)
                losses = overall.get('losses', 0)
                avg_score = overall.get('average_score', 0)
                
                print(f"{team_key}: {wins}-{losses} record, {avg_score:.1f} avg points")
        
        betting_analysis = analysis.get('betting_analysis', {})
        if betting_analysis.get('key_factors'):
            print(f"\n🎯 KEY FACTORS:")
            for factor in betting_analysis['key_factors']:
                print(f"  • {factor}")
        
        print(f"\n💾 Detailed analysis saved to data/ directory")
    
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
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())