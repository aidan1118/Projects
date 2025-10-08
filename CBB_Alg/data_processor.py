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
        """Get trends for a specific team using actual game statistics"""
        team = format_team_name(team)
        
        # Validate team exists
        teams_data = self.load_teams_data()
        team_info = find_team_info(team, teams_data)
        if not team_info:
            raise ValueError(f"Team '{team}' not found")
        
        logger.info(f"Fetching game statistics for {team_info.get('School', team)}")
        
        # Try different approaches to get actual game statistics
        try:
            # Use season stats (more reliable than individual games)
            season_stats = self.api_client.get_team_stats('2025')
            team_season_data = next((s for s in season_stats if s.get('Team') == team), None)
            if team_season_data:
                trends_data = self._calculate_season_trends(team_season_data, team_info)
            else:
                # Try different season formats
                for season_format in ['2025', '2024', '2023-24']:
                    try:
                        logger.info(f"Trying season format: {season_format}")
                        season_stats = self.api_client.get_team_stats(season_format)
                        team_season_data = next((s for s in season_stats if s.get('Team') == team), None)
                        if team_season_data:
                            trends_data = self._calculate_season_trends(team_season_data, team_info)
                            break
                    except Exception as season_e:
                        logger.info(f"Season format {season_format} failed: {season_e}")
                        continue
                else:
                    # Try to get games data instead
                    try:
                        games_data = self.api_client.get_games('2025')
                        team_games = [g for g in games_data if g.get('HomeTeam') == team or g.get('AwayTeam') == team]
                        if team_games:
                            trends_data = self._calculate_trends_from_games(team_games, team, team_info)
                        else:
                            raise Exception("No game data found")
                    except Exception as games_e:
                        logger.warning(f"Games data also failed: {games_e}")
                        # Last resort: use betting trends but mark as such
                        logger.warning(f"Using betting trends for {team} - no stats available")
                        trends_data = self.api_client.get_team_trends(team)
                        trends_data['_data_source'] = 'betting_trends'
                        
        except Exception as e:
            logger.warning(f"All stats methods failed for {team}: {e}")
            # Fallback to betting trends
            trends_data = self.api_client.get_team_trends(team)
            trends_data['_data_source'] = 'betting_trends'
        
        # Save raw data
        filename = f"team_trends_{team}_{self._get_timestamp()}.json"
        save_json(trends_data, filename)
        
        return trends_data
    
    def _calculate_game_trends(self, team_games: list, team_info: dict) -> Dict[Any, Any]:
        """Calculate performance trends from game-by-game statistics"""
        # Sort games by date (most recent first)
        sorted_games = sorted(team_games, key=lambda x: x.get('DateTime', ''), reverse=True)
        
        trends_data = {
            'Team': team_info.get('Key', ''),
            'TeamGameTrends': [],
            '_data_source': 'game_statistics'
        }
        
        # Calculate trends for different game ranges
        trend_ranges = [
            ('Last 3 Games', 3),
            ('Last 5 Games', 5), 
            ('Last 10 Games', 10),
            ('Season Total', len(sorted_games))
        ]
        
        for scope, count in trend_ranges:
            games_subset = sorted_games[:count] if count < len(sorted_games) else sorted_games
            
            if games_subset:
                wins = sum(1 for g in games_subset if g.get('Points', 0) > g.get('OpponentPoints', 0))
                losses = len(games_subset) - wins
                avg_score = sum(g.get('Points', 0) for g in games_subset) / len(games_subset)
                avg_opp_score = sum(g.get('OpponentPoints', 0) for g in games_subset) / len(games_subset)
                
                trend = {
                    'Scope': scope,
                    'Wins': wins,
                    'Losses': losses,
                    'Games': len(games_subset),
                    'AverageScore': round(avg_score, 1),
                    'AverageOpponentScore': round(avg_opp_score, 1)
                }
                trends_data['TeamGameTrends'].append(trend)
        
        return trends_data
    
    def _calculate_season_trends(self, season_data: dict, team_info: dict) -> Dict[Any, Any]:
        """Calculate trends from season statistics with detailed breakdown"""
        games = season_data.get('Games', 0)
        total_points = season_data.get('Points', 0)
        total_opp_points = season_data.get('OpponentPoints', 0)
        
        # Calculate proper averages (total points / games played)
        avg_score = round(total_points / games, 1) if games > 0 else 0
        avg_opp_score = round(total_opp_points / games, 1) if games > 0 and total_opp_points > 0 else 0
        
        # Calculate shooting stats
        fg_made = season_data.get('FieldGoalsMade', 0)
        fg_attempted = season_data.get('FieldGoalsAttempted', 0)
        fg_pct = round(season_data.get('FieldGoalsPercentage', 0), 1)
        
        three_made = season_data.get('ThreePointersMade', 0)
        three_attempted = season_data.get('ThreePointersAttempted', 0)
        three_pct = round(season_data.get('ThreePointersPercentage', 0), 1)
        
        ft_made = season_data.get('FreeThrowsMade', 0)
        ft_attempted = season_data.get('FreeThrowsAttempted', 0)
        ft_pct = round(season_data.get('FreeThrowsPercentage', 0), 1)
        
        trends_data = {
            'Team': team_info.get('Key', ''),
            'TeamGameTrends': [{
                'Scope': 'Season Total',
                'Wins': season_data.get('Wins', 0),
                'Losses': season_data.get('Losses', 0),
                'Games': games,
                'AverageScore': avg_score,
                'AverageOpponentScore': avg_opp_score
            }],
            'DetailedStats': {
                'Shooting': {
                    'FieldGoals': f"{fg_made}/{fg_attempted} ({fg_pct}%)" if fg_attempted > 0 else "N/A",
                    'ThreePointers': f"{three_made}/{three_attempted} ({three_pct}%)" if three_attempted > 0 else "N/A",
                    'FreeThrows': f"{ft_made}/{ft_attempted} ({ft_pct}%)" if ft_attempted > 0 else "N/A"
                },
                'PerGame': {
                    'Points': avg_score,
                    'FieldGoals': round(fg_made / games, 1) if games > 0 else 0,
                    'ThreePointers': round(three_made / games, 1) if games > 0 else 0,
                    'FreeThrows': round(ft_made / games, 1) if games > 0 else 0,
                    'Rebounds': round(season_data.get('Rebounds', 0) / games, 1) if games > 0 else 0,
                    'Assists': round(season_data.get('Assists', 0) / games, 1) if games > 0 else 0,
                    'Steals': round(season_data.get('Steals', 0) / games, 1) if games > 0 else 0,
                    'Blocks': round(season_data.get('BlockedShots', 0) / games, 1) if games > 0 else 0,
                    'Turnovers': round(season_data.get('Turnovers', 0) / games, 1) if games > 0 else 0
                }
            },
            '_data_source': 'season_statistics'
        }
        
        return trends_data
    
    def _calculate_trends_from_games(self, games: list, team: str, team_info: dict) -> Dict[Any, Any]:
        """Calculate performance trends from games data"""
        # Filter and sort games by date (most recent first)
        team_games = []
        for game in games:
            if game.get('HomeTeam') == team:
                team_games.append({
                    'DateTime': game.get('DateTime', ''),
                    'Points': game.get('HomeTeamScore', 0),
                    'OpponentPoints': game.get('AwayTeamScore', 0),
                    'Opponent': game.get('AwayTeam', ''),
                    'IsHome': True
                })
            elif game.get('AwayTeam') == team:
                team_games.append({
                    'DateTime': game.get('DateTime', ''),
                    'Points': game.get('AwayTeamScore', 0),
                    'OpponentPoints': game.get('HomeTeamScore', 0),
                    'Opponent': game.get('HomeTeam', ''),
                    'IsHome': False
                })
        
        # Sort by date (most recent first)
        sorted_games = sorted(team_games, key=lambda x: x.get('DateTime', ''), reverse=True)
        
        trends_data = {
            'Team': team_info.get('Key', ''),
            'TeamGameTrends': [],
            '_data_source': 'games_data'
        }
        
        # Calculate trends for different game ranges
        trend_ranges = [
            ('Last 3 Games', 3),
            ('Last 5 Games', 5), 
            ('Last 10 Games', 10),
            ('Season Total', len(sorted_games))
        ]
        
        for scope, count in trend_ranges:
            games_subset = sorted_games[:count] if count < len(sorted_games) else sorted_games
            
            if games_subset:
                wins = sum(1 for g in games_subset if g.get('Points', 0) > g.get('OpponentPoints', 0))
                losses = len(games_subset) - wins
                avg_score = sum(g.get('Points', 0) for g in games_subset) / len(games_subset)
                avg_opp_score = sum(g.get('OpponentPoints', 0) for g in games_subset) / len(games_subset)
                
                trend = {
                    'Scope': scope,
                    'Wins': wins,
                    'Losses': losses,
                    'Games': len(games_subset),
                    'AverageScore': round(avg_score, 1),
                    'AverageOpponentScore': round(avg_opp_score, 1)
                }
                trends_data['TeamGameTrends'].append(trend)
        
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