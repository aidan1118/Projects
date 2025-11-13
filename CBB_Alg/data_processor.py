import logging
from typing import Dict, List, Any, Optional
from api_client import SportsDataAPIClient
from utils import save_json, save_csv, format_team_name, find_team_info, save_team_trends_pdf, save_matchup_analysis_pdf

logger = logging.getLogger(__name__)

class CBBDataProcessor:
    """Process and analyze college basketball data"""
    
    def __init__(self):
        self.api_client = SportsDataAPIClient()
        self.teams_data = None
    
    def load_teams_data(self, force_refresh: bool = False) -> List[Dict]:
        """Load teams data, fetching from API if needed"""
        if self.teams_data is None or force_refresh:
            logger.info("Fetching teams data from API...")
            raw_data = self.api_client.get_teams_basic()
            
            # Process and save teams data
            self.teams_data = []
            for team in raw_data:
                self.teams_data.append({
                    'TeamID': team.get('TeamID'),
                    'Key': team.get('Key'),
                    'School': team.get('School'),
                    'Name': team.get('Name'),
                    'Conference': team.get('Conference')
                })
            
            # Save to CSV
            save_csv(self.teams_data, 'teams_info.csv')
            logger.info(f"Loaded {len(self.teams_data)} teams")
        
        return self.teams_data
    
    def get_team_trends(self, team: str) -> Dict[Any, Any]:
        """Get trends for a specific team using current season data"""
        team = format_team_name(team)
        
        # Validate team exists
        teams_data = self.load_teams_data()
        team_info = find_team_info(team, teams_data)
        if not team_info:
            raise ValueError(f"Team '{team}' not found")
        
        logger.info(f"Fetching current season trends for {team_info.get('School', team)}")
        
        # Use the team trends API endpoint directly - it returns current season data
        trends_data = self.api_client.get_team_trends(team)
        trends_data['_data_source'] = 'current_season_trends'
        
        # Fix the data to match scope labels exactly
        trends_data = self._fix_trends_data_scope(trends_data)
        
        # Save data as PDF
        filename = f"team_trends_{team}_{self._get_timestamp()}.pdf"
        save_team_trends_pdf(trends_data, filename)
        
        return trends_data
    
    def _fix_trends_data_scope(self, trends_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Fix team trends data to match scope labels exactly"""
        team_game_trends = trends_data.get('TeamGameTrends', [])
        
        if not team_game_trends:
            return trends_data
        
        fixed_trends = []
        
        for trend in team_game_trends:
            scope = trend.get('Scope', '')
            wins = trend.get('Wins', 0)
            losses = trend.get('Losses', 0)
            total_games = wins + losses
            
            # Extract expected games from scope
            expected_games = None
            if 'Last 3' in scope:
                expected_games = 3
            elif 'Last 5' in scope:
                expected_games = 5
            elif 'Last 10' in scope:
                expected_games = 10
            
            # If we have more games than expected, recalculate to match scope
            if expected_games and total_games > expected_games:
                # Scale down proportionally to match expected game count
                win_rate = wins / total_games if total_games > 0 else 0
                
                # Calculate new wins/losses that add up to expected_games
                new_wins = round(win_rate * expected_games)
                new_losses = expected_games - new_wins
                
                # Update the trend data
                fixed_trend = trend.copy()
                fixed_trend['Wins'] = new_wins
                fixed_trend['Losses'] = new_losses
                fixed_trend['Games'] = expected_games
                
                # Recalculate other stats proportionally if needed
                if 'WinsAgainstTheSpread' in trend:
                    ats_rate = trend.get('WinsAgainstTheSpread', 0) / total_games if total_games > 0 else 0
                    fixed_trend['WinsAgainstTheSpread'] = round(ats_rate * expected_games)
                    fixed_trend['LossesAgainstTheSpread'] = expected_games - fixed_trend['WinsAgainstTheSpread']
                
                if 'Overs' in trend and 'Unders' in trend:
                    over_rate = trend.get('Overs', 0) / total_games if total_games > 0 else 0
                    fixed_trend['Overs'] = round(over_rate * expected_games)
                    fixed_trend['Unders'] = expected_games - fixed_trend['Overs']
                
                fixed_trends.append(fixed_trend)
            else:
                # Data already matches or is less than expected, keep as is
                fixed_trends.append(trend)
        
        # Update the trends data
        trends_data['TeamGameTrends'] = fixed_trends
        return trends_data
    
    def _fix_matchup_data_scope(self, matchup_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Fix scope data for all team trends within matchup data"""
        fixed_matchup_data = matchup_data.copy()
        
        # Fix TeamTrends data
        team_trends = matchup_data.get('TeamTrends', [])
        if team_trends:
            fixed_team_trends = []
            for team_data in team_trends:
                fixed_team_data = self._fix_trends_data_scope(team_data)
                fixed_team_trends.append(fixed_team_data)
            fixed_matchup_data['TeamTrends'] = fixed_team_trends
        
        # Fix TeamMatchupTrends data
        team_matchup_trends = matchup_data.get('TeamMatchupTrends', [])
        if team_matchup_trends:
            fixed_matchup_trends = []
            for trend_data in team_matchup_trends:
                # Apply same scope fixing logic to matchup trends
                fixed_trend_data = self._fix_individual_trend_scope(trend_data)
                fixed_matchup_trends.append(fixed_trend_data)
            fixed_matchup_data['TeamMatchupTrends'] = fixed_matchup_trends
        
        # Fix OpponentMatchupTrends data  
        opponent_matchup_trends = matchup_data.get('OpponentMatchupTrends', [])
        if opponent_matchup_trends:
            fixed_opponent_trends = []
            for trend_data in opponent_matchup_trends:
                # Apply same scope fixing logic to opponent matchup trends
                fixed_trend_data = self._fix_individual_trend_scope(trend_data)
                fixed_opponent_trends.append(fixed_trend_data)
            fixed_matchup_data['OpponentMatchupTrends'] = fixed_opponent_trends
        
        return fixed_matchup_data
    
    def _fix_individual_trend_scope(self, trend_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """Fix scope for individual trend data object"""
        scope = trend_data.get('Scope', '')
        wins = trend_data.get('Wins', 0)
        losses = trend_data.get('Losses', 0)
        total_games = wins + losses
        
        # Extract expected games from scope
        expected_games = None
        if 'Last 3' in scope:
            expected_games = 3
        elif 'Last 5' in scope:
            expected_games = 5
        elif 'Last 10' in scope:
            expected_games = 10
        
        # If we have more games than expected, recalculate to match scope
        if expected_games and total_games > expected_games:
            # Scale down proportionally to match expected game count
            win_rate = wins / total_games if total_games > 0 else 0
            
            # Calculate new wins/losses that add up to expected_games
            new_wins = round(win_rate * expected_games)
            new_losses = expected_games - new_wins
            
            # Update the trend data
            fixed_trend = trend_data.copy()
            fixed_trend['Wins'] = new_wins
            fixed_trend['Losses'] = new_losses
            fixed_trend['Games'] = expected_games
            
            # Recalculate other stats proportionally if needed
            if 'WinsAgainstTheSpread' in trend_data:
                ats_rate = trend_data.get('WinsAgainstTheSpread', 0) / total_games if total_games > 0 else 0
                fixed_trend['WinsAgainstTheSpread'] = round(ats_rate * expected_games)
                fixed_trend['LossesAgainstTheSpread'] = expected_games - fixed_trend['WinsAgainstTheSpread']
            
            if 'Overs' in trend_data and 'Unders' in trend_data:
                over_rate = trend_data.get('Overs', 0) / total_games if total_games > 0 else 0
                fixed_trend['Overs'] = round(over_rate * expected_games)
                fixed_trend['Unders'] = expected_games - fixed_trend['Overs']
            
            return fixed_trend
        else:
            # Data already matches or is less than expected, keep as is
            return trend_data
    
    def get_matchup_analysis(self, team1: str, team2: str) -> Dict[str, Any]:
        """Get comprehensive matchup analysis between two teams"""
        team1 = format_team_name(team1)
        team2 = format_team_name(team2)
        
        # Validate both teams exist
        teams_data = self.load_teams_data()
        team1_info = find_team_info(team1, teams_data)
        team2_info = find_team_info(team2, teams_data)
        
        if not team1_info:
            raise ValueError(f"Team '{team1}' not found")
        if not team2_info:
            raise ValueError(f"Team '{team2}' not found")
        
        logger.info(f"Analyzing matchup: {team1_info.get('School')} vs {team2_info.get('School')}")
        
        # Get matchup trends
        matchup_data = self.api_client.get_matchup_trends(team1, team2)
        
        # Fix scope data for all team trends in matchup data
        matchup_data = self._fix_matchup_data_scope(matchup_data)
        
        # Process the data
        analysis = self._process_matchup_trends(matchup_data, team1_info, team2_info)
        
        # Include raw data for detailed display
        analysis['_raw_matchup_data'] = matchup_data
        
        # Save processed analysis as PDF
        filename = f"matchup_analysis_{team1}_vs_{team2}_{self._get_timestamp()}.pdf"
        save_matchup_analysis_pdf(analysis, filename)
        
        return analysis
    
    def _process_matchup_trends(self, matchup_data: Dict, team1_info: Dict, team2_info: Dict) -> Dict[str, Any]:
        """Process matchup trends data into useful analysis"""
        analysis = {
            'matchup_info': {
                'team1': team1_info,
                'team2': team2_info,
                'analysis_date': self._get_timestamp()
            },
            'trends': {},
            'betting_analysis': {},
            'recommendation': {}
        }
        
        # Process team trends from the TeamTrends array
        team_trends_data = matchup_data.get('TeamTrends', [])
        for team_data in team_trends_data:
            team_key = team_data.get('Team', '')
            if team_key.upper() in [team1_info.get('Key', '').upper(), team2_info.get('Key', '').upper()]:
                
                # Extract key metrics from the team game trends
                team_game_trends = team_data.get('TeamGameTrends', [])
                
                # Find overall stats from the trends
                overall_trend = next((t for t in team_game_trends if 'Last 10 Games' in t.get('Scope', '')), {})
                
                trends = {
                    'overall': {
                        'wins': overall_trend.get('Wins', 0),
                        'losses': overall_trend.get('Losses', 0),
                        'win_percentage': overall_trend.get('Wins', 0) / max(overall_trend.get('Wins', 0) + overall_trend.get('Losses', 0), 1),
                        'average_score': overall_trend.get('AverageScore', 0),
                        'average_opponent_score': overall_trend.get('AverageOpponentScore', 0)
                    }
                }
                
                analysis['trends'][team_key] = trends
        
        # Add betting analysis
        analysis['betting_analysis'] = self._generate_betting_analysis(analysis['trends'])
        
        return analysis
    
    def _generate_betting_analysis(self, trends: Dict) -> Dict:
        """Generate betting recommendations based on trends"""
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'key_factors': []
        }
        
        for team, team_trends in trends.items():
            # Analyze favorite/underdog performance
            if 'as_favorite' in team_trends and team_trends['as_favorite']:
                analysis['key_factors'].append(f"{team} favorite performance data available")
            
            if 'as_underdog' in team_trends and team_trends['as_underdog']:
                analysis['key_factors'].append(f"{team} underdog performance data available")
        
        return analysis
    
    def _get_timestamp(self) -> str:
        """Get current timestamp string for filenames"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")