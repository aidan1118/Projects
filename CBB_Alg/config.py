import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for CBB prediction system"""
    
    # API Configuration - with free tier default key for easy setup
    SPORTSDATA_API_KEY = os.getenv('SPORTSDATA_API_KEY', '236607118e034379b0b004f76f2f48d6')
    SPORTSDATA_STATS_API_KEY = os.getenv('SPORTSDATA_STATS_API_KEY')
    SPORTSDATA_BASE_URL = os.getenv('SPORTSDATA_BASE_URL', 'https://api.sportsdata.io/v3/cbb')
    
    # Default settings
    DEFAULT_SEASON = os.getenv('DEFAULT_SEASON', '2025')
    DEFAULT_SEASON_TYPE = os.getenv('DEFAULT_SEASON_TYPE', 'REG')
    
    # Data directories
    DATA_DIR = 'data'
    OUTPUT_DIR = 'output'
    
    # API endpoints
    ENDPOINTS = {
        'teams_basic': '/scores/json/TeamsBasic',
        'team_trends': '/odds/json/TeamTrends/{team}',
        'matchup_trends': '/odds/json/MatchupTrends/{team}/{opponent}',
        'games': '/scores/json/Games/{season}',
        'player_stats': '/stats/json/PlayerSeasonStats/{season}',
        'team_stats': '/stats/json/TeamSeasonStats/{season}',
        'team_game_stats': '/stats/json/TeamGameStats/{season}',
        'game_results': '/scores/json/GamesByDate/{date}'
    }
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        if not cls.SPORTSDATA_API_KEY:
            raise ValueError("SPORTSDATA_API_KEY not found in environment variables")
        
        if not cls.SPORTSDATA_BASE_URL:
            raise ValueError("SPORTSDATA_BASE_URL not found in environment variables")
    
    @classmethod
    def get_endpoint_url(cls, endpoint_name, **kwargs):
        """Get full URL for an endpoint"""
        if endpoint_name not in cls.ENDPOINTS:
            raise ValueError(f"Unknown endpoint: {endpoint_name}")
        
        endpoint = cls.ENDPOINTS[endpoint_name].format(**kwargs)
        return f"{cls.SPORTSDATA_BASE_URL}{endpoint}"