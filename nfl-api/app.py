from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import nfl_data_py as nfl
from datetime import datetime, timedelta
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "NFL Data API for Power BI",
        "endpoints": {
            "/nfl/games": "Get NFL games data",
            "/nfl/stats": "Get player statistics", 
            "/nfl/teams": "Get team information",
            "/nfl/bye-weeks": "Get bye week schedule for each team",
            "/nfl/team-stats": "Get aggregated team statistics with bye week analysis",
            "/nfl/team-performance": "Get team scoring performance before/after bye weeks"
        }
    })

@app.route('/nfl/games')
def get_games():
    try:
        year = request.args.get('year', datetime.now().year)
        week = request.args.get('week', None)
        
        logger.info(f"Fetching games for year: {year}, week: {week}")
        
        games = nfl.import_schedules([int(year)])
        if week:
            games = games[games['week'] == int(week)]
        
        # Select relevant columns
        relevant_cols = ['game_id', 'season', 'week', 'gameday', 'home_team', 'away_team', 
                        'home_score', 'away_score', 'result', 'total']
        # Only include columns that exist
        available_cols = [col for col in relevant_cols if col in games.columns]
        games = games[available_cols]
        
        # Convert to dict and handle NaN values
        games_dict = games.fillna('').to_dict('records')
        
        return jsonify({
            "data": games_dict,
            "count": len(games_dict)
        })
        
    except Exception as e:
        logger.error(f"Error fetching games: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/nfl/stats')
def get_stats():
    try:
        year = request.args.get('year', datetime.now().year)
        stat_type = request.args.get('type', 'passing')
        
        logger.info(f"Fetching {stat_type} stats for year: {year}")
        
        stats = nfl.import_weekly_data([int(year)])
        
        if stat_type == 'passing':
            passing_cols = ['player_id', 'player_name', 'recent_team', 'season', 'week', 
                           'passing_yards', 'passing_tds', 'interceptions', 'completions', 'attempts']
            available_cols = [col for col in passing_cols if col in stats.columns]
            stats = stats[available_cols]
            stats = stats[stats['attempts'] > 0] if 'attempts' in stats.columns else stats
        elif stat_type == 'rushing':
            rushing_cols = ['player_id', 'player_name', 'recent_team', 'season', 'week', 
                           'rushing_yards', 'rushing_tds', 'carries']
            available_cols = [col for col in rushing_cols if col in stats.columns]
            stats = stats[available_cols]
            stats = stats[stats['carries'] > 0] if 'carries' in stats.columns else stats
        elif stat_type == 'receiving':
            receiving_cols = ['player_id', 'player_name', 'recent_team', 'season', 'week', 
                             'receiving_yards', 'receiving_tds', 'receptions', 'targets']
            available_cols = [col for col in receiving_cols if col in stats.columns]
            stats = stats[available_cols]
            stats = stats[stats['targets'] > 0] if 'targets' in stats.columns else stats
        else:
            return jsonify({"error": "Invalid stat type. Use: passing, rushing, or receiving"}), 400
        
        # Convert to dict and handle NaN values
        stats_dict = stats.fillna(0).to_dict('records')
        
        return jsonify({
            "data": stats_dict,
            "count": len(stats_dict),
            "stat_type": stat_type
        })
        
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/nfl/teams')
def get_teams():
    try:
        teams = nfl.import_team_desc()
        teams_dict = teams.to_dict('records')
        
        return jsonify({
            "data": teams_dict,
            "count": len(teams_dict)
        })
        
    except Exception as e:
        logger.error(f"Error fetching teams: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/nfl/bye-weeks')
def get_bye_weeks():
    try:
        year = request.args.get('year', datetime.now().year)
        logger.info(f"Fetching bye weeks for year: {year}")
        
        schedule = nfl.import_schedules([int(year)])
        all_teams = set(schedule['home_team'].unique()) | set(schedule['away_team'].unique())
        
        bye_weeks = {}
        for week in range(1, 19):  # NFL weeks 1-18
            week_games = schedule[schedule['week'] == week]
            teams_playing = set(week_games['home_team'].unique()) | set(week_games['away_team'].unique())
            teams_on_bye = all_teams - teams_playing
            if teams_on_bye:
                bye_weeks[week] = list(teams_on_bye)
        
        # Convert to list format for easier Power BI consumption
        bye_data = []
        for week, teams in bye_weeks.items():
            for team in teams:
                bye_data.append({
                    "season": int(year),
                    "team": team,
                    "bye_week": week
                })
        
        return jsonify({
            "data": bye_data,
            "count": len(bye_data)
        })
        
    except Exception as e:
        logger.error(f"Error fetching bye weeks: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/nfl/team-stats')
def get_team_stats():
    try:
        year = request.args.get('year', datetime.now().year)
        team = request.args.get('team', None)
        before_bye = request.args.get('before_bye', 'false').lower() == 'true'
        after_bye = request.args.get('after_bye', 'false').lower() == 'true'
        
        logger.info(f"Fetching team stats for year: {year}, team: {team}, before_bye: {before_bye}, after_bye: {after_bye}")
        
        # Get bye weeks first
        schedule = nfl.import_schedules([int(year)])
        all_teams = set(schedule['home_team'].unique()) | set(schedule['away_team'].unique())
        
        bye_weeks_map = {}
        for week in range(1, 19):
            week_games = schedule[schedule['week'] == week]
            teams_playing = set(week_games['home_team'].unique()) | set(week_games['away_team'].unique())
            teams_on_bye = all_teams - teams_playing
            for bye_team in teams_on_bye:
                bye_weeks_map[bye_team] = week
        
        # Get weekly stats
        stats = nfl.import_weekly_data([int(year)])
        
        # Aggregate by team and week
        team_stats = []
        
        teams_to_process = [team] if team else all_teams
        
        for team_code in teams_to_process:
            team_bye_week = bye_weeks_map.get(team_code)
            if not team_bye_week:
                continue
                
            # Filter stats for this team
            team_data = stats[stats['recent_team'] == team_code]
            
            # Define week ranges
            if before_bye:
                weeks_filter = team_data['week'] < team_bye_week
                period = "before_bye"
            elif after_bye:
                weeks_filter = team_data['week'] > team_bye_week
                period = "after_bye"
            else:
                weeks_filter = team_data['week'] != team_bye_week  # All non-bye weeks
                period = "full_season"
            
            period_data = team_data[weeks_filter]
            
            # Aggregate stats
            if len(period_data) > 0:
                agg_stats = {
                    "season": int(year),
                    "team": team_code,
                    "bye_week": team_bye_week,
                    "period": period,
                    "games_played": len(period_data['week'].unique()),
                    
                    # Offensive stats
                    "total_passing_yards": period_data['passing_yards'].sum(),
                    "total_passing_tds": period_data['passing_tds'].sum(),
                    "total_rushing_yards": period_data['rushing_yards'].sum(), 
                    "total_rushing_tds": period_data['rushing_tds'].sum(),
                    "total_receiving_yards": period_data['receiving_yards'].sum(),
                    "total_receiving_tds": period_data['receiving_tds'].sum(),
                    
                    # Per game averages
                    "avg_passing_yards": period_data.groupby('week')['passing_yards'].sum().mean() if 'passing_yards' in period_data.columns else 0,
                    "avg_rushing_yards": period_data.groupby('week')['rushing_yards'].sum().mean() if 'rushing_yards' in period_data.columns else 0,
                    "avg_receiving_yards": period_data.groupby('week')['receiving_yards'].sum().mean() if 'receiving_yards' in period_data.columns else 0,
                }
                
                team_stats.append(agg_stats)
        
        return jsonify({
            "data": team_stats,
            "count": len(team_stats)
        })
        
    except Exception as e:
        logger.error(f"Error fetching team stats: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/nfl/team-performance')
def get_team_performance():
    try:
        year = request.args.get('year', datetime.now().year)
        team = request.args.get('team', None)
        
        logger.info(f"Fetching team performance for year: {year}, team: {team}")
        
        # Get schedule and bye weeks
        schedule = nfl.import_schedules([int(year)])
        all_teams = set(schedule['home_team'].unique()) | set(schedule['away_team'].unique())
        
        bye_weeks_map = {}
        for week in range(1, 19):
            week_games = schedule[schedule['week'] == week]
            teams_playing = set(week_games['home_team'].unique()) | set(week_games['away_team'].unique())
            teams_on_bye = all_teams - teams_playing
            for bye_team in teams_on_bye:
                bye_weeks_map[bye_team] = week
        
        # Get weekly stats for offensive calculations
        stats = nfl.import_weekly_data([int(year)])
        
        performance_data = []
        teams_to_process = [team] if team else all_teams
        
        for team_code in teams_to_process:
            team_bye_week = bye_weeks_map.get(team_code)
            if not team_bye_week:
                continue
                
            # Get team games
            team_games = schedule[
                (schedule['home_team'] == team_code) | 
                (schedule['away_team'] == team_code)
            ].copy()
            
            # Calculate team scores and opponent scores
            team_games['team_score'] = team_games.apply(
                lambda row: row['home_score'] if row['home_team'] == team_code else row['away_score'], axis=1
            )
            team_games['opponent_score'] = team_games.apply(
                lambda row: row['away_score'] if row['home_team'] == team_code else row['home_score'], axis=1
            )
            team_games['is_home'] = team_games['home_team'] == team_code
            
            # Get team offensive stats
            team_stats = stats[stats['recent_team'] == team_code]
            
            # Split by bye week
            before_bye_games = team_games[team_games['week'] < team_bye_week]
            after_bye_games = team_games[team_games['week'] > team_bye_week]
            before_bye_stats = team_stats[team_stats['week'] < team_bye_week]
            after_bye_stats = team_stats[team_stats['week'] > team_bye_week]
            
            # Calculate before bye stats
            if len(before_bye_games) > 0:
                # Calculate passing stats per game
                before_passing_weekly = before_bye_stats.groupby('week').agg({
                    'passing_yards': 'sum',
                    'passing_tds': 'sum'
                }) if 'passing_yards' in before_bye_stats.columns else pd.DataFrame()
                
                # Calculate rushing stats per game  
                before_rushing_weekly = before_bye_stats.groupby('week').agg({
                    'rushing_yards': 'sum',
                    'rushing_tds': 'sum'
                }) if 'rushing_yards' in before_bye_stats.columns else pd.DataFrame()
                
                before_stats = {
                    "season": int(year),
                    "team": team_code,
                    "bye_week": team_bye_week,
                    "period": "before_bye",
                    "games_played": len(before_bye_games),
                    "total_points_scored": before_bye_games['team_score'].sum(),
                    "total_points_allowed": before_bye_games['opponent_score'].sum(),
                    "avg_points_scored": before_bye_games['team_score'].mean(),
                    "avg_points_allowed": before_bye_games['opponent_score'].mean(),
                    "wins": len(before_bye_games[before_bye_games['team_score'] > before_bye_games['opponent_score']]),
                    "losses": len(before_bye_games[before_bye_games['team_score'] < before_bye_games['opponent_score']]),
                    "home_games": len(before_bye_games[before_bye_games['is_home']]),
                    "away_games": len(before_bye_games[~before_bye_games['is_home']]),
                    
                    # Passing stats
                    "total_passing_yards": float(before_passing_weekly['passing_yards'].sum()) if not before_passing_weekly.empty else 0,
                    "total_passing_tds": int(before_passing_weekly['passing_tds'].sum()) if not before_passing_weekly.empty else 0,
                    "avg_passing_yards": float(before_passing_weekly['passing_yards'].mean()) if not before_passing_weekly.empty else 0,
                    "avg_passing_tds": float(before_passing_weekly['passing_tds'].mean()) if not before_passing_weekly.empty else 0,
                    
                    # Rushing stats
                    "total_rushing_yards": float(before_rushing_weekly['rushing_yards'].sum()) if not before_rushing_weekly.empty else 0,
                    "total_rushing_tds": int(before_rushing_weekly['rushing_tds'].sum()) if not before_rushing_weekly.empty else 0,
                    "avg_rushing_yards": float(before_rushing_weekly['rushing_yards'].mean()) if not before_rushing_weekly.empty else 0,
                    "avg_rushing_tds": float(before_rushing_weekly['rushing_tds'].mean()) if not before_rushing_weekly.empty else 0
                }
                performance_data.append(before_stats)
            
            # Calculate after bye stats
            if len(after_bye_games) > 0:
                # Calculate passing stats per game
                after_passing_weekly = after_bye_stats.groupby('week').agg({
                    'passing_yards': 'sum',
                    'passing_tds': 'sum'
                }) if 'passing_yards' in after_bye_stats.columns else pd.DataFrame()
                
                # Calculate rushing stats per game
                after_rushing_weekly = after_bye_stats.groupby('week').agg({
                    'rushing_yards': 'sum', 
                    'rushing_tds': 'sum'
                }) if 'rushing_yards' in after_bye_stats.columns else pd.DataFrame()
                
                after_stats = {
                    "season": int(year),
                    "team": team_code,
                    "bye_week": team_bye_week,
                    "period": "after_bye",
                    "games_played": len(after_bye_games),
                    "total_points_scored": after_bye_games['team_score'].sum(),
                    "total_points_allowed": after_bye_games['opponent_score'].sum(),
                    "avg_points_scored": after_bye_games['team_score'].mean(),
                    "avg_points_allowed": after_bye_games['opponent_score'].mean(),
                    "wins": len(after_bye_games[after_bye_games['team_score'] > after_bye_games['opponent_score']]),
                    "losses": len(after_bye_games[after_bye_games['team_score'] < after_bye_games['opponent_score']]),
                    "home_games": len(after_bye_games[after_bye_games['is_home']]),
                    "away_games": len(after_bye_games[~after_bye_games['is_home']]),
                    
                    # Passing stats
                    "total_passing_yards": float(after_passing_weekly['passing_yards'].sum()) if not after_passing_weekly.empty else 0,
                    "total_passing_tds": int(after_passing_weekly['passing_tds'].sum()) if not after_passing_weekly.empty else 0,
                    "avg_passing_yards": float(after_passing_weekly['passing_yards'].mean()) if not after_passing_weekly.empty else 0,
                    "avg_passing_tds": float(after_passing_weekly['passing_tds'].mean()) if not after_passing_weekly.empty else 0,
                    
                    # Rushing stats
                    "total_rushing_yards": float(after_rushing_weekly['rushing_yards'].sum()) if not after_rushing_weekly.empty else 0,
                    "total_rushing_tds": int(after_rushing_weekly['rushing_tds'].sum()) if not after_rushing_weekly.empty else 0,
                    "avg_rushing_yards": float(after_rushing_weekly['rushing_yards'].mean()) if not after_rushing_weekly.empty else 0,
                    "avg_rushing_tds": float(after_rushing_weekly['rushing_tds'].mean()) if not after_rushing_weekly.empty else 0
                }
                performance_data.append(after_stats)
        
        return jsonify({
            "data": performance_data,
            "count": len(performance_data)
        })
        
    except Exception as e:
        logger.error(f"Error fetching team performance: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)