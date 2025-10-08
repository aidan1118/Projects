import requests
import json
import logging
from typing import Dict, Any, Optional
from config import Config

logger = logging.getLogger(__name__)

class SportsDataAPIClient:
    """Centralized API client for SportsData.io college basketball API"""
    
    def __init__(self):
        Config.validate_config()
        self.api_key = Config.SPORTSDATA_API_KEY
        self.stats_api_key = Config.SPORTSDATA_STATS_API_KEY
        self.base_url = Config.SPORTSDATA_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CBB-Prediction-System/1.0'
        })
    
    def _make_request(self, url: str, params: Optional[Dict] = None, use_stats_key: bool = False) -> Dict[Any, Any]:
        """Make a request to the API with error handling"""
        try:
            # Add API key as URL parameter (SportsData.io uses this method)
            if params is None:
                params = {}
            # Use stats API key for statistical endpoints, regular key for others
            api_key = self.stats_api_key if use_stats_key and self.stats_api_key else self.api_key
            params['key'] = api_key
            
            logger.info(f"Making API request to: {url}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            raise Exception("API request timed out")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            if response.status_code == 401:
                raise Exception("Invalid API key or unauthorized access")
            elif response.status_code == 429:
                raise Exception("API rate limit exceeded")
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise Exception(f"API request failed: {str(e)}")
        
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response")
            raise Exception("Invalid JSON response from API")
    
    def get_teams_basic(self) -> Dict[Any, Any]:
        """Get basic information for all teams"""
        url = Config.get_endpoint_url('teams_basic')
        return self._make_request(url)
    
    def get_team_trends(self, team: str) -> Dict[Any, Any]:
        """Get trends for a specific team"""
        url = Config.get_endpoint_url('team_trends', team=team)
        return self._make_request(url)
    
    def get_matchup_trends(self, team: str, opponent: str) -> Dict[Any, Any]:
        """Get matchup trends between two teams"""
        url = Config.get_endpoint_url('matchup_trends', team=team, opponent=opponent)
        return self._make_request(url)
    
    def get_games(self, season: str = None) -> Dict[Any, Any]:
        """Get games for a season"""
        if season is None:
            season = Config.DEFAULT_SEASON
        url = Config.get_endpoint_url('games', season=season)
        return self._make_request(url, use_stats_key=True)
    
    def get_player_stats(self, season: str = None) -> Dict[Any, Any]:
        """Get player statistics for a season"""
        if season is None:
            season = Config.DEFAULT_SEASON
        url = Config.get_endpoint_url('player_stats', season=season)
        return self._make_request(url, use_stats_key=True)
    
    def get_team_stats(self, season: str = None) -> Dict[Any, Any]:
        """Get team season statistics"""
        if season is None:
            season = Config.DEFAULT_SEASON
        url = Config.get_endpoint_url('team_stats', season=season)
        return self._make_request(url, use_stats_key=True)
    
    def get_team_game_stats(self, season: str = None) -> Dict[Any, Any]:
        """Get team game-by-game statistics"""
        if season is None:
            season = Config.DEFAULT_SEASON
        url = Config.get_endpoint_url('team_game_stats', season=season)
        return self._make_request(url, use_stats_key=True)
    
    def get_game_results_by_date(self, date: str) -> Dict[Any, Any]:
        """Get game results by date (YYYY-MM-DD format)"""
        url = Config.get_endpoint_url('game_results', date=date)
        return self._make_request(url)