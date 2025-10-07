import logging
from typing import Dict, List, Any, Optional
from api_client import SportsDataAPIClient
from utils import save_json, save_csv, format_team_name, find_team_info

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
        """Get trends for a specific team"""
        team = format_team_name(team)
        
        # Validate team exists
        teams_data = self.load_teams_data()
        team_info = find_team_info(team, teams_data)
        if not team_info:
            raise ValueError(f"Team '{team}' not found")
        
        logger.info(f"Fetching trends for {team_info.get('School', team)}")
        trends_data = self.api_client.get_team_trends(team)
        
        # Save raw data
        filename = f"team_trends_{team}_{self._get_timestamp()}.json"
        save_json(trends_data, filename)
        
        return trends_data
    
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
        
        # Process the data
        analysis = self._process_matchup_trends(matchup_data, team1_info, team2_info)
        
        # Save processed analysis
        filename = f"matchup_analysis_{team1}_vs_{team2}_{self._get_timestamp()}.json"
        save_json(analysis, filename)
        
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
        
        # Process team trends
        for team_data in matchup_data:
            team_key = team_data.get('Team', '')
            if team_key.upper() in [team1_info.get('Key', '').upper(), team2_info.get('Key', '').upper()]:
                
                # Extract key metrics
                trends = {
                    'as_favorite': self._extract_trend_stats(team_data, 'Favorite'),
                    'as_underdog': self._extract_trend_stats(team_data, 'Underdog'),
                    'at_home': self._extract_trend_stats(team_data, 'Home'),
                    'away': self._extract_trend_stats(team_data, 'Away'),
                    'overall': self._extract_overall_stats(team_data)
                }
                
                analysis['trends'][team_key] = trends
        
        # Add betting analysis
        analysis['betting_analysis'] = self._generate_betting_analysis(analysis['trends'])
        
        return analysis
    
    def _extract_trend_stats(self, team_data: Dict, context: str) -> Dict:
        """Extract trend statistics for a specific context"""
        stats = {}
        
        # Look for relevant keys in the data
        for key, value in team_data.items():
            if context.lower() in key.lower() and isinstance(value, (int, float)):
                stats[key] = value
        
        return stats
    
    def _extract_overall_stats(self, team_data: Dict) -> Dict:
        """Extract overall team statistics"""
        return {
            'wins': team_data.get('Wins', 0),
            'losses': team_data.get('Losses', 0),
            'win_percentage': team_data.get('Percentage', 0),
            'average_score': team_data.get('AverageScore', 0),
            'average_opponent_score': team_data.get('AverageOpponentScore', 0)
        }
    
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
        """Get timestamp for file naming"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")