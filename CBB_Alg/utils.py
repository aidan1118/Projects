import logging
import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Any
from config import Config
from fpdf import FPDF

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

def save_team_trends_pdf(data: Dict[Any, Any], filename: str, directory: str = None) -> str:
    """Save team trends data to PDF file"""
    if directory is None:
        directory = Config.DATA_DIR
    
    ensure_directories()
    pdf_filename = filename.replace('.json', '.pdf')
    filepath = os.path.join(directory, pdf_filename)
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Title
        team_name = data.get('Team', 'Unknown Team')
        pdf.cell(0, 10, f'Team Analysis: {team_name}', ln=True, align='C')
        pdf.ln(5)
        
        # Upcoming game
        upcoming = data.get('UpcomingGame', {})
        if upcoming:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, 'Upcoming Game:', ln=True)
            pdf.set_font('Arial', '', 10)
            away_team = upcoming.get('AwayTeam', 'TBD')
            home_team = upcoming.get('HomeTeam', 'TBD')
            date_time = upcoming.get('DateTime', 'TBD')
            channel = upcoming.get('Channel', 'TBD')
            pdf.cell(0, 6, f'{away_team} @ {home_team}', ln=True)
            pdf.cell(0, 6, f'Date: {date_time}', ln=True)
            pdf.cell(0, 6, f'TV: {channel}', ln=True)
            pdf.ln(5)
        
        # Team trends
        trends = data.get('TeamGameTrends', [])
        if trends:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, 'Recent Performance:', ln=True)
            pdf.set_font('Arial', 'B', 9)
            pdf.cell(50, 6, 'Scope', 1)
            pdf.cell(20, 6, 'Record', 1)
            pdf.cell(25, 6, 'Avg Score', 1)
            pdf.cell(25, 6, 'Opp Score', 1)
            pdf.cell(20, 6, 'ATS', 1)
            pdf.cell(20, 6, 'O/U', 1)
            pdf.ln()
            
            pdf.set_font('Arial', '', 8)
            for trend in trends[:10]:  # Show top 10 trends
                scope = trend.get('Scope', '')[:25]
                wins = trend.get('Wins', 0)
                losses = trend.get('Losses', 0)
                avg_score = trend.get('AverageScore', 0)
                avg_opp = trend.get('AverageOpponentScore', 0)
                ats_wins = trend.get('WinsAgainstTheSpread', 0)
                ats_losses = trend.get('LossesAgainstTheSpread', 0)
                overs = trend.get('Overs', 0)
                unders = trend.get('Unders', 0)
                
                # Use calculated total games for display
                total_games = wins + losses
                record_text = f'{wins}-{losses}'
                
                pdf.cell(50, 5, scope, 1)
                pdf.cell(20, 5, record_text, 1)
                pdf.cell(25, 5, f'{avg_score:.1f}', 1)
                pdf.cell(25, 5, f'{avg_opp:.1f}', 1)
                pdf.cell(20, 5, f'{ats_wins}-{ats_losses}', 1)
                pdf.cell(20, 5, f'{overs}-{unders}', 1)
                pdf.ln()
        
        pdf.ln(5)
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 5, f'Report generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
        
        pdf.output(filepath)
        logging.info(f"PDF saved to: {filepath}")
        return filepath
    
    except Exception as e:
        logging.error(f"Failed to save PDF to {filepath}: {e}")
        # Still save JSON as fallback
        return save_json(data, filename, directory)

def save_matchup_analysis_pdf(data: Dict[Any, Any], filename: str, directory: str = None) -> str:
    """Save comprehensive matchup analysis data to PDF file"""
    if directory is None:
        directory = Config.DATA_DIR
    
    ensure_directories()
    pdf_filename = filename.replace('.json', '.pdf')
    filepath = os.path.join(directory, pdf_filename)
    
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        
        # Title
        matchup_info = data.get('matchup_info', {})
        team1_info = matchup_info.get('team1', {})
        team2_info = matchup_info.get('team2', {})
        team1_name = team1_info.get('School', 'Team 1')
        team2_name = team2_info.get('School', 'Team 2')
        team1_key = team1_info.get('Key', 'T1')
        team2_key = team2_info.get('Key', 'T2')
        
        pdf.cell(0, 10, f'Matchup Analysis', ln=True, align='C')
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 8, f'{team1_name} vs {team2_name}', ln=True, align='C')
        pdf.ln(5)
        
        # Get raw matchup data for detailed breakdowns
        raw_data = data.get('_raw_matchup_data', {})
        team_trends_data = raw_data.get('TeamTrends', [])
        
        # Detailed team performance for both teams
        for team_data in team_trends_data:
            team_key = team_data.get('Team', '')
            school_name = team1_name if team_key == team1_key else team2_name
            
            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, f'{school_name} ({team_key})', ln=True)
            pdf.ln(3)
            
            # Upcoming game
            upcoming = team_data.get('UpcomingGame', {})
            if upcoming:
                away = upcoming.get('AwayTeam', 'TBD')
                home = upcoming.get('HomeTeam', 'TBD')
                date = upcoming.get('DateTime', 'TBD')[:10] if upcoming.get('DateTime') else 'TBD'
                channel = upcoming.get('Channel', 'TBD')
                
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 6, f'Next Game: {away} @ {home} on {date} ({channel})', ln=True)
                pdf.ln(2)
            
            # Recent performance table
            game_trends = team_data.get('TeamGameTrends', [])
            if game_trends:
                pdf.set_font('Arial', 'B', 10)
                pdf.cell(0, 6, 'Recent Performance:', ln=True)
                
                # Table headers
                pdf.set_font('Arial', 'B', 8)
                pdf.cell(35, 5, 'Scope', 1)
                pdf.cell(20, 5, 'Record', 1)
                pdf.cell(20, 5, 'Avg Score', 1)
                pdf.cell(20, 5, 'Opp Score', 1)
                pdf.cell(20, 5, 'Point Diff', 1)
                pdf.ln()
                
                pdf.set_font('Arial', '', 7)
                for trend in game_trends[:8]:
                    scope = trend.get('Scope', '')[:20]
                    wins = trend.get('Wins', 0)
                    losses = trend.get('Losses', 0)
                    avg_score = trend.get('AverageScore', 0)
                    avg_opp = trend.get('AverageOpponentScore', 0)
                    point_diff = avg_score - avg_opp
                    
                    pdf.cell(35, 4, scope, 1)
                    pdf.cell(20, 4, f'{wins}-{losses}', 1)
                    pdf.cell(20, 4, f'{avg_score:.1f}', 1)
                    pdf.cell(20, 4, f'{avg_opp:.1f}', 1)
                    pdf.cell(20, 4, f'{point_diff:+.1f}', 1)
                    pdf.ln()
            
            pdf.ln(5)
        
        # Head-to-head history if available
        previous_games = raw_data.get('PreviousGames', [])
        if previous_games:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, 'Head-to-Head History:', ln=True)
            pdf.ln(2)
            
            pdf.set_font('Arial', 'B', 8)
            pdf.cell(25, 5, 'Date', 1)
            pdf.cell(25, 5, 'Away Team', 1)
            pdf.cell(20, 5, 'Score', 1)
            pdf.cell(25, 5, 'Home Team', 1)
            pdf.cell(30, 5, 'Winner', 1)
            pdf.ln()
            
            pdf.set_font('Arial', '', 7)
            for game in previous_games[:10]:
                date = game.get('DateTime', '')[:10] if game.get('DateTime') else 'Unknown'
                away_team = game.get('AwayTeam', '')[:12]
                home_team = game.get('HomeTeam', '')[:12]
                away_score = game.get('AwayTeamScore', 0)
                home_score = game.get('HomeTeamScore', 0)
                winner = home_team if home_score > away_score else away_team
                
                pdf.cell(25, 4, date, 1)
                pdf.cell(25, 4, away_team, 1)
                pdf.cell(20, 4, f'{away_score}-{home_score}', 1)
                pdf.cell(25, 4, home_team, 1)
                pdf.cell(30, 4, winner[:15], 1)
                pdf.ln()
        
        # Key factors and analysis
        betting_analysis = data.get('betting_analysis', {})
        key_factors = betting_analysis.get('key_factors', [])
        if key_factors:
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, 'Key Betting Factors:', ln=True)
            pdf.set_font('Arial', '', 9)
            for factor in key_factors:
                pdf.cell(0, 5, f'• {factor}', ln=True)
        
        pdf.ln(5)
        pdf.set_font('Arial', '', 8)
        pdf.cell(0, 5, f'Analysis generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
        
        pdf.output(filepath)
        logging.info(f"PDF saved to: {filepath}")
        return filepath
    
    except Exception as e:
        logging.error(f"Failed to save PDF to {filepath}: {e}")
        # Still save JSON as fallback
        return save_json(data, filename, directory)