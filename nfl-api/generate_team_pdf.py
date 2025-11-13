#!/usr/bin/env python3

import requests
import json
import pandas as pd
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Set style for professional looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# NFL Team mappings
NFL_TEAMS = {
    'ARI': 'Arizona Cardinals',
    'ATL': 'Atlanta Falcons', 
    'BAL': 'Baltimore Ravens',
    'BUF': 'Buffalo Bills',
    'CAR': 'Carolina Panthers',
    'CHI': 'Chicago Bears',
    'CIN': 'Cincinnati Bengals',
    'CLE': 'Cleveland Browns',
    'DAL': 'Dallas Cowboys',
    'DEN': 'Denver Broncos',
    'DET': 'Detroit Lions',
    'GB': 'Green Bay Packers',
    'HOU': 'Houston Texans',
    'IND': 'Indianapolis Colts',
    'JAX': 'Jacksonville Jaguars',
    'KC': 'Kansas City Chiefs',
    'LV': 'Las Vegas Raiders',
    'LAC': 'Los Angeles Chargers',
    'LA': 'Los Angeles Rams',
    'MIA': 'Miami Dolphins',
    'MIN': 'Minnesota Vikings',
    'NE': 'New England Patriots',
    'NO': 'New Orleans Saints',
    'NYG': 'New York Giants',
    'NYJ': 'New York Jets',
    'PHI': 'Philadelphia Eagles',
    'PIT': 'Pittsburgh Steelers',
    'SF': 'San Francisco 49ers',
    'SEA': 'Seattle Seahawks',
    'TB': 'Tampa Bay Buccaneers',
    'TEN': 'Tennessee Titans',
    'WAS': 'Washington Commanders'
}

def fetch_api_data(endpoint):
    """Fetch data from API endpoint"""
    try:
        url = f"http://localhost:5001{endpoint}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint}: {e}")
        return None

def generate_team_report(team_code, year=2024):
    """Generate comprehensive team report"""
    if team_code not in NFL_TEAMS:
        print(f"❌ Invalid team code: {team_code}")
        print("Valid team codes:", ", ".join(sorted(NFL_TEAMS.keys())))
        return None
        
    team_name = NFL_TEAMS[team_code]
    print(f"🏈 Generating {team_name} Report...")
    
    # Fetch team-related data
    endpoints = {
        'team_performance': f'/nfl/team-performance?year={year}&team={team_code}',
        'bye_weeks': f'/nfl/bye-weeks?year={year}',
        'games': f'/nfl/games?year={year}',
        'teams': '/nfl/teams'
    }
    
    data = {}
    for name, endpoint in endpoints.items():
        print(f"📊 Fetching {name}...")
        result = fetch_api_data(endpoint)
        if result:
            data[name] = result
    
    # Process data for specific team
    print(f"🔍 Processing {team_name} data...")
    
    report_data = {
        'team_code': team_code,
        'team_name': team_name,
        'year': year,
        'team_info': {},
        'bye_week_info': {},
        'performance_summary': {},
        'games': []
    }
    
    # Team Information
    if 'teams' in data:
        for team in data['teams']['data']:
            if team.get('team_abbr') == team_code:
                report_data['team_info'] = team
                break
    
    # Bye Week Information  
    if 'bye_weeks' in data:
        for bye in data['bye_weeks']['data']:
            if bye['team'] == team_code:
                report_data['bye_week_info'] = bye
                break
    
    # Performance Summary
    if 'team_performance' in data:
        report_data['performance_summary'] = data['team_performance']['data']
    
    # Games (filter for team games)
    if 'games' in data:
        for game in data['games']['data']:
            if game.get('home_team') == team_code or game.get('away_team') == team_code:
                # Add team-specific info
                game['team_score'] = game.get('home_score', 0) if game.get('home_team') == team_code else game.get('away_score', 0)
                game['opponent_score'] = game.get('away_score', 0) if game.get('home_team') == team_code else game.get('home_score', 0)
                game['opponent'] = game.get('away_team') if game.get('home_team') == team_code else game.get('home_team')
                game['home_game'] = game.get('home_team') == team_code
                
                if game['team_score'] and game['opponent_score']:
                    game['result'] = 'W' if game['team_score'] > game['opponent_score'] else ('L' if game['team_score'] < game['opponent_score'] else 'T')
                else:
                    game['result'] = '-'
                    
                report_data['games'].append(game)
    
    return report_data

def create_title_page(pdf, data):
    """Create title page for the PDF report"""
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor('white')
    
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 8.5, f"{data['team_name']}", fontsize=32, fontweight='bold', 
            ha='center', va='center')
    ax.text(5, 7.8, f"{data['year']} Season Analysis Report", fontsize=20, 
            ha='center', va='center', style='italic')
    
    # Team Info Box
    if data['team_info']:
        info_text = f"""Conference: {data['team_info'].get('team_conf', 'N/A')}
Division: {data['team_info'].get('team_division', 'N/A')}
Bye Week: Week {data['bye_week_info'].get('bye_week', 'N/A')}"""
    else:
        info_text = f"Team Code: {data['team_code']}\nBye Week: Week {data['bye_week_info'].get('bye_week', 'N/A')}"
    
    ax.text(5, 6, info_text, fontsize=14, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    
    # Report metadata
    ax.text(5, 3, f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
            fontsize=12, ha='center', va='center')
    ax.text(5, 2.5, "NFL Analytics Platform", fontsize=10, ha='center', va='center', 
            style='italic', color='gray')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

def create_performance_summary_page(pdf, data):
    """Create performance summary page"""
    if not data['performance_summary']:
        return
        
    fig = plt.figure(figsize=(8.5, 11))
    fig.suptitle(f"{data['team_name']} - Bye Week Performance Analysis", 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Get before/after data
    before_bye = next((p for p in data['performance_summary'] if p['period'] == 'before_bye'), {})
    after_bye = next((p for p in data['performance_summary'] if p['period'] == 'after_bye'), {})
    
    if not before_bye or not after_bye:
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "Performance data not available", 
                ha='center', va='center', transform=ax.transAxes, fontsize=16)
        ax.axis('off')
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()
        return
    
    # Create comparison table
    metrics = [
        ('Games Played', before_bye.get('games_played', 0), after_bye.get('games_played', 0)),
        ('Wins', before_bye.get('wins', 0), after_bye.get('wins', 0)),
        ('Losses', before_bye.get('losses', 0), after_bye.get('losses', 0)),
        ('Points Scored/Game', f"{before_bye.get('avg_points_scored', 0):.1f}", 
         f"{after_bye.get('avg_points_scored', 0):.1f}"),
        ('Points Allowed/Game', f"{before_bye.get('avg_points_allowed', 0):.1f}", 
         f"{after_bye.get('avg_points_allowed', 0):.1f}"),
        ('Passing Yards/Game', f"{before_bye.get('avg_passing_yards', 0):.1f}", 
         f"{after_bye.get('avg_passing_yards', 0):.1f}"),
        ('Rushing Yards/Game', f"{before_bye.get('avg_rushing_yards', 0):.1f}", 
         f"{after_bye.get('avg_rushing_yards', 0):.1f}"),
        ('Win Percentage', f"{before_bye.get('wins', 0)/max(before_bye.get('games_played', 1), 1):.3f}", 
         f"{after_bye.get('wins', 0)/max(after_bye.get('games_played', 1), 1):.3f}")
    ]
    
    # Create table
    ax = fig.add_subplot(111)
    ax.axis('tight')
    ax.axis('off')
    
    table_data = []
    for metric, before_val, after_val in metrics:
        table_data.append([metric, str(before_val), str(after_val)])
    
    table = ax.table(cellText=table_data,
                    colLabels=['Metric', 'Before Bye', 'After Bye'],
                    cellLoc='center',
                    loc='center',
                    bbox=[0.1, 0.3, 0.8, 0.5])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 2)
    
    # Style the table
    for i in range(len(table_data) + 1):
        for j in range(3):
            cell = table[(i, j)]
            if i == 0:  # Header row
                cell.set_facecolor('#4472C4')
                cell.set_text_props(weight='bold', color='white')
            else:
                if i % 2 == 0:
                    cell.set_facecolor('#F8F8F8')
                else:
                    cell.set_facecolor('#FFFFFF')
    
    # Add notes
    plt.figtext(0.1, 0.2, f"Bye Week: Week {data['bye_week_info'].get('bye_week', 'N/A')}", 
                fontsize=12, fontweight='bold')
    plt.figtext(0.1, 0.15, f"Total Games: {before_bye.get('games_played', 0) + after_bye.get('games_played', 0)}", 
                fontsize=10)
    plt.figtext(0.1, 0.12, f"Season Record: {before_bye.get('wins', 0) + after_bye.get('wins', 0)}-{before_bye.get('losses', 0) + after_bye.get('losses', 0)}", 
                fontsize=10)
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

def create_games_schedule_page(pdf, data):
    """Create games schedule page"""
    if not data['games']:
        return
        
    fig = plt.figure(figsize=(8.5, 11))
    fig.suptitle(f"{data['team_name']} - {data['year']} Season Games", 
                 fontsize=16, fontweight='bold', y=0.95)
    
    # Sort games by week
    sorted_games = sorted(data['games'], key=lambda x: x.get('week', 0))
    
    # Prepare table data
    table_data = []
    for game in sorted_games:
        week = game.get('week', 'N/A')
        date = game.get('gameday', 'N/A')
        opponent = game.get('opponent', 'N/A')
        location = "vs" if game.get('home_game') else "@"
        team_score = game.get('team_score', '-')
        opp_score = game.get('opponent_score', '-')
        result = game.get('result', '-')
        
        table_data.append([f"Week {week}", date, f"{location} {opponent}", 
                          f"{team_score}-{opp_score}", result])
    
    # Create table
    ax = fig.add_subplot(111)
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=table_data,
                    colLabels=['Week', 'Date', 'Opponent', 'Score', 'Result'],
                    cellLoc='center',
                    loc='center',
                    bbox=[0.05, 0.1, 0.9, 0.8])
    
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    
    # Style the table
    for i in range(len(table_data) + 1):
        for j in range(5):
            cell = table[(i, j)]
            if i == 0:  # Header row
                cell.set_facecolor('#4472C4')
                cell.set_text_props(weight='bold', color='white')
            else:
                if i % 2 == 0:
                    cell.set_facecolor('#F8F8F8')
                else:
                    cell.set_facecolor('#FFFFFF')
                    
                # Color code results
                if j == 4:  # Result column
                    if table_data[i-1][4] == 'W':
                        cell.set_facecolor('#E8F5E8')
                    elif table_data[i-1][4] == 'L':
                        cell.set_facecolor('#FFE8E8')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

def create_team_pdf_report(data):
    """Create comprehensive PDF report for the team"""
    filename = f"{data['team_code'].lower()}_{data['year']}_report.pdf"
    
    print(f"📄 Creating PDF report: {filename}")
    
    with PdfPages(filename) as pdf:
        # Page 1: Title page
        create_title_page(pdf, data)
        
        # Page 2: Performance summary
        create_performance_summary_page(pdf, data)
        
        # Page 3: Games schedule
        create_games_schedule_page(pdf, data)
        
        # Set PDF metadata
        d = pdf.infodict()
        d['Title'] = f"{data['team_name']} - {data['year']} Season Report"
        d['Author'] = "NFL Analytics Platform"
        d['Subject'] = f"Team performance analysis for {data['team_name']}"
        d['Keywords'] = f"NFL, {data['year']}, {data['team_code']}, {data['team_name']}, Statistics"
        d['CreationDate'] = datetime.now()
    
    return filename

def main():
    parser = argparse.ArgumentParser(description='Generate NFL team PDF report')
    parser.add_argument('team', nargs='?', help='NFL team code (e.g., BUF, KC, SF)')
    parser.add_argument('--year', type=int, default=2024, help='Season year (default: 2024)')
    parser.add_argument('--list-teams', action='store_true', help='List all available team codes')
    
    args = parser.parse_args()
    
    if args.list_teams:
        print("Available NFL Team Codes:")
        print("=" * 50)
        for code, name in sorted(NFL_TEAMS.items()):
            print(f"{code:3} - {name}")
        return
    
    if not args.team:
        parser.error("Team code is required unless using --list-teams")
        return
    
    # Generate report
    report_data = generate_team_report(args.team.upper(), args.year)
    
    if report_data:
        # Create PDF report
        pdf_filename = create_team_pdf_report(report_data)
        
        # Also save JSON data
        json_filename = f"{args.team.lower()}_{args.year}_data.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"✅ PDF report generated: {pdf_filename}")
        print(f"📊 Raw data saved: {json_filename}")
        print(f"🏈 Report for: {report_data['team_name']}")
        
    else:
        print("❌ Failed to generate report. Make sure the API is running on localhost:5001")
        print("   Start the API with: python app.py")

if __name__ == "__main__":
    main()