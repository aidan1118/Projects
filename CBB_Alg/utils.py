import logging
import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Any
from config import Config

def setup_logging(level: str = 'INFO') -> logging.Logger:
    """Setup logging configuration"""
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('cbb_prediction.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def ensure_directories():
    """Ensure required directories exist"""
    directories = [Config.DATA_DIR, Config.OUTPUT_DIR]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

def save_json(data: Dict[Any, Any], filename: str, directory: str = None) -> str:
    """Save data to JSON file"""
    if directory is None:
        directory = Config.DATA_DIR
    
    ensure_directories()
    filepath = os.path.join(directory, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Data saved to: {filepath}")
        return filepath
    
    except Exception as e:
        logging.error(f"Failed to save JSON to {filepath}: {e}")
        raise

def load_json(filename: str, directory: str = None) -> Dict[Any, Any]:
    """Load data from JSON file"""
    if directory is None:
        directory = Config.DATA_DIR
    
    filepath = os.path.join(directory, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logging.info(f"Data loaded from: {filepath}")
        return data
    
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logging.error(f"Failed to load JSON from {filepath}: {e}")
        raise

def save_csv(data: List[Dict], filename: str, directory: str = None) -> str:
    """Save data to CSV file"""
    if directory is None:
        directory = Config.DATA_DIR
    
    ensure_directories()
    filepath = os.path.join(directory, filename)
    
    if not data:
        logging.warning("No data to save to CSV")
        return filepath
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        logging.info(f"Data saved to CSV: {filepath}")
        return filepath
    
    except Exception as e:
        logging.error(f"Failed to save CSV to {filepath}: {e}")
        raise

def format_team_name(team: str) -> str:
    """Format team name/abbreviation to uppercase"""
    return team.upper().strip()

def get_timestamp() -> str:
    """Get current timestamp string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def validate_team_abbreviation(team: str, teams_data: List[Dict]) -> bool:
    """Validate if team abbreviation exists in teams data"""
    team = format_team_name(team)
    return any(t.get('Key', '').upper() == team for t in teams_data)

def find_team_info(team: str, teams_data: List[Dict]) -> Dict:
    """Find team information by abbreviation"""
    team = format_team_name(team)
    for t in teams_data:
        if t.get('Key', '').upper() == team:
            return t
    return {}