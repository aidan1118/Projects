#!/usr/bin/env python3
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

# Set style for professional looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def load_team_data():
    """Load team performance data from JSON file"""
    with open('team_performance.json', 'r') as f:
        data = json.load(f)
    return data['data']

def create_team_comparison_df(data):
    """Create a DataFrame with before/after bye comparisons"""
    teams = {}
    
    for record in data:
        team = record['team']
        period = record['period']
        
        if team not in teams:
            teams[team] = {}
        
        teams[team][period] = record
    
    # Convert to comparison format
    comparison_data = []
    for team, periods in teams.items():
        if 'before_bye' in periods and 'after_bye' in periods:
            before = periods['before_bye']
            after = periods['after_bye']
            
            comparison_data.append({
                'team': team,
                'bye_week': before['bye_week'],
                # Before bye stats
                'before_total_passing_yards': before['total_passing_yards'],
                'before_total_rushing_yards': before['total_rushing_yards'],
                'before_total_points_scored': before['total_points_scored'],
                'before_total_points_allowed': before['total_points_allowed'],
                'before_wins': before['wins'],
                'before_losses': before['losses'],
                'before_games_played': before['games_played'],
                # After bye stats  
                'after_total_passing_yards': after['total_passing_yards'],
                'after_total_rushing_yards': after['total_rushing_yards'],
                'after_total_points_scored': after['total_points_scored'],
                'after_total_points_allowed': after['total_points_allowed'],
                'after_wins': after['wins'],
                'after_losses': after['losses'],
                'after_games_played': after['games_played'],
                # Calculated per-game averages
                'before_ppg_scored': before['total_points_scored'] / before['games_played'] if before['games_played'] > 0 else 0,
                'after_ppg_scored': after['total_points_scored'] / after['games_played'] if after['games_played'] > 0 else 0,
                'before_ppg_allowed': before['total_points_allowed'] / before['games_played'] if before['games_played'] > 0 else 0,
                'after_ppg_allowed': after['total_points_allowed'] / after['games_played'] if after['games_played'] > 0 else 0,
                'before_rushing_ypg': before['total_rushing_yards'] / before['games_played'] if before['games_played'] > 0 else 0,
                'after_rushing_ypg': after['total_rushing_yards'] / after['games_played'] if after['games_played'] > 0 else 0,
                'before_passing_ypg': before['total_passing_yards'] / before['games_played'] if before['games_played'] > 0 else 0,
                'after_passing_ypg': after['total_passing_yards'] / after['games_played'] if after['games_played'] > 0 else 0,
                'before_win_pct': before['wins'] / before['games_played'] if before['games_played'] > 0 else 0,
                'after_win_pct': after['wins'] / after['games_played'] if after['games_played'] > 0 else 0,
            })
    
    return pd.DataFrame(comparison_data)

def create_summary_stats_page(pdf, df):
    """Create a summary statistics page"""
    fig = plt.figure(figsize=(11, 8.5))
    fig.suptitle('NFL 2024 Season: Pre vs Post Bye Week Performance Summary', fontsize=16, fontweight='bold', y=0.95)
    
    # Calculate summary statistics
    stats = {
        'Metric': [
            'Average Points Scored Per Game',
            'Average Points Allowed Per Game', 
            'Average Rushing Yards Per Game',
            'Average Passing Yards Per Game',
            'Average Win Percentage'
        ],
        'Before Bye': [
            f"{df['before_ppg_scored'].mean():.1f}",
            f"{df['before_ppg_allowed'].mean():.1f}",
            f"{df['before_rushing_ypg'].mean():.0f}",
            f"{df['before_passing_ypg'].mean():.0f}",
            f"{df['before_win_pct'].mean():.3f}"
        ],
        'After Bye': [
            f"{df['after_ppg_scored'].mean():.1f}",
            f"{df['after_ppg_allowed'].mean():.1f}",
            f"{df['after_rushing_ypg'].mean():.0f}",
            f"{df['after_passing_ypg'].mean():.0f}",
            f"{df['after_win_pct'].mean():.3f}"
        ],
        'Difference': [
            f"{df['after_ppg_scored'].mean() - df['before_ppg_scored'].mean():+.1f}",
            f"{df['after_ppg_allowed'].mean() - df['before_ppg_allowed'].mean():+.1f}",
            f"{df['after_rushing_ypg'].mean() - df['before_rushing_ypg'].mean():+.0f}",
            f"{df['after_passing_ypg'].mean() - df['before_passing_ypg'].mean():+.0f}",
            f"{df['after_win_pct'].mean() - df['before_win_pct'].mean():+.3f}"
        ]
    }
    
    # Create table
    ax = fig.add_subplot(111)
    ax.axis('tight')
    ax.axis('off')
    
    table_data = []
    for i in range(len(stats['Metric'])):
        table_data.append([stats['Metric'][i], stats['Before Bye'][i], 
                          stats['After Bye'][i], stats['Difference'][i]])
    
    table = ax.table(cellText=table_data,
                    colLabels=['Metric', 'Before Bye', 'After Bye', 'Difference'],
                    cellLoc='left',
                    loc='center',
                    bbox=[0.05, 0.3, 0.9, 0.5])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2.5)
    
    # Adjust column widths
    cellDict = table.get_celld()
    for i in range(len(table_data) + 1):
        cellDict[(i, 0)].set_width(0.5)  # Metric column - wider
        cellDict[(i, 1)].set_width(0.15)  # Before Bye
        cellDict[(i, 2)].set_width(0.15)  # After Bye  
        cellDict[(i, 3)].set_width(0.2)   # Difference
    
    # Style the table
    for i in range(len(table_data) + 1):
        for j in range(4):
            cell = table[(i, j)]
            if i == 0:  # Header row
                cell.set_facecolor('#4472C4')
                cell.set_text_props(weight='bold', color='white')
            else:
                if j == 3:  # Difference column
                    val = float(stats['Difference'][i-1].replace('+', ''))
                    if val > 0:
                        cell.set_facecolor('#E8F5E8')
                    elif val < 0:
                        cell.set_facecolor('#FFE8E8')
                    else:
                        cell.set_facecolor('#F8F8F8')
                else:
                    cell.set_facecolor('#F8F8F8')
    
    # Add notes
    plt.figtext(0.1, 0.2, "Notes:", fontsize=12, fontweight='bold')
    plt.figtext(0.1, 0.15, "• Positive differences (green) indicate improved performance after bye week", fontsize=10)
    plt.figtext(0.1, 0.12, "• Negative differences (red) indicate worse performance after bye week", fontsize=10)
    plt.figtext(0.1, 0.09, "• Analysis includes all 32 NFL teams for the 2024 season", fontsize=10)
    plt.figtext(0.1, 0.06, f"• Report generated on {datetime.now().strftime('%B %d, %Y')}", fontsize=10)
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

def create_offense_comparison_charts(pdf, df):
    """Create offensive performance comparison charts"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(11, 8.5))
    fig.suptitle('Offensive Performance: Before vs After Bye Week', fontsize=14, fontweight='bold')
    
    # Points scored per game
    ax1.scatter(df['before_ppg_scored'], df['after_ppg_scored'], alpha=0.7, s=60)
    ax1.plot([0, df[['before_ppg_scored', 'after_ppg_scored']].max().max()], 
             [0, df[['before_ppg_scored', 'after_ppg_scored']].max().max()], 
             'r--', alpha=0.5, label='Equal performance')
    # Add team labels
    for idx, row in df.iterrows():
        ax1.annotate(row['team'], (row['before_ppg_scored'], row['after_ppg_scored']), 
                    xytext=(3, 3), textcoords='offset points', fontsize=8, alpha=0.8)
    ax1.set_xlabel('Points Per Game (Before Bye)')
    ax1.set_ylabel('Points Per Game (After Bye)')
    ax1.set_title('Points Scored Per Game')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Rushing yards per game  
    ax2.scatter(df['before_rushing_ypg'], df['after_rushing_ypg'], alpha=0.7, s=60, color='green')
    ax2.plot([0, df[['before_rushing_ypg', 'after_rushing_ypg']].max().max()], 
             [0, df[['before_rushing_ypg', 'after_rushing_ypg']].max().max()], 
             'r--', alpha=0.5, label='Equal performance')
    # Add team labels
    for idx, row in df.iterrows():
        ax2.annotate(row['team'], (row['before_rushing_ypg'], row['after_rushing_ypg']), 
                    xytext=(3, 3), textcoords='offset points', fontsize=8, alpha=0.8)
    ax2.set_xlabel('Rushing Yards Per Game (Before Bye)')
    ax2.set_ylabel('Rushing Yards Per Game (After Bye)')
    ax2.set_title('Rushing Yards Per Game')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Passing yards per game
    ax3.scatter(df['before_passing_ypg'], df['after_passing_ypg'], alpha=0.7, s=60, color='orange')
    ax3.plot([0, df[['before_passing_ypg', 'after_passing_ypg']].max().max()], 
             [0, df[['before_passing_ypg', 'after_passing_ypg']].max().max()], 
             'r--', alpha=0.5, label='Equal performance')
    # Add team labels
    for idx, row in df.iterrows():
        ax3.annotate(row['team'], (row['before_passing_ypg'], row['after_passing_ypg']), 
                    xytext=(3, 3), textcoords='offset points', fontsize=8, alpha=0.8)
    ax3.set_xlabel('Passing Yards Per Game (Before Bye)')
    ax3.set_ylabel('Passing Yards Per Game (After Bye)')
    ax3.set_title('Passing Yards Per Game')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Win percentage
    ax4.scatter(df['before_win_pct'], df['after_win_pct'], alpha=0.7, s=60, color='purple')
    ax4.plot([0, 1], [0, 1], 'r--', alpha=0.5, label='Equal performance')
    # Add team labels
    for idx, row in df.iterrows():
        ax4.annotate(row['team'], (row['before_win_pct'], row['after_win_pct']), 
                    xytext=(3, 3), textcoords='offset points', fontsize=8, alpha=0.8)
    ax4.set_xlabel('Win Percentage (Before Bye)')
    ax4.set_ylabel('Win Percentage (After Bye)')
    ax4.set_title('Win Percentage')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

def create_team_performance_charts(pdf, df):
    """Create individual team performance comparison charts"""
    # Sort teams by improvement in points scored
    df['ppg_improvement'] = df['after_ppg_scored'] - df['before_ppg_scored']
    df_sorted = df.sort_values('ppg_improvement', ascending=True)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8.5))
    fig.suptitle('Team-by-Team Performance Changes After Bye Week', fontsize=14, fontweight='bold')
    
    # Points per game improvement
    colors1 = ['red' if x < 0 else 'green' for x in df_sorted['ppg_improvement']]
    bars1 = ax1.barh(range(len(df_sorted)), df_sorted['ppg_improvement'], color=colors1, alpha=0.7)
    ax1.set_yticks(range(len(df_sorted)))
    ax1.set_yticklabels(df_sorted['team'], fontsize=8)
    ax1.set_xlabel('Change in Points Per Game')
    ax1.set_title('Points Scored Per Game: Change After Bye Week')
    ax1.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars1, df_sorted['ppg_improvement'])):
        ax1.text(val + (0.2 if val >= 0 else -0.2), i, f'{val:+.1f}', 
                va='center', ha='left' if val >= 0 else 'right', fontsize=7)
    
    # Win percentage improvement
    df_sorted['win_pct_improvement'] = df_sorted['after_win_pct'] - df_sorted['before_win_pct']
    df_sorted = df_sorted.sort_values('win_pct_improvement', ascending=True)
    colors2 = ['red' if x < 0 else 'green' for x in df_sorted['win_pct_improvement']]
    bars2 = ax2.barh(range(len(df_sorted)), df_sorted['win_pct_improvement'], color=colors2, alpha=0.7)
    ax2.set_yticks(range(len(df_sorted)))
    ax2.set_yticklabels(df_sorted['team'], fontsize=8)
    ax2.set_xlabel('Change in Win Percentage')
    ax2.set_title('Win Percentage: Change After Bye Week')
    ax2.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars2, df_sorted['win_pct_improvement'])):
        ax2.text(val + (0.02 if val >= 0 else -0.02), i, f'{val:+.3f}', 
                va='center', ha='left' if val >= 0 else 'right', fontsize=7)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

def create_defensive_comparison_chart(pdf, df):
    """Create defensive performance comparison chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 8.5))
    fig.suptitle('Defensive Performance: Before vs After Bye Week', fontsize=14, fontweight='bold')
    
    # Points allowed per game scatter plot
    ax1.scatter(df['before_ppg_allowed'], df['after_ppg_allowed'], alpha=0.7, s=60, color='red')
    ax1.plot([0, df[['before_ppg_allowed', 'after_ppg_allowed']].max().max()], 
             [0, df[['before_ppg_allowed', 'after_ppg_allowed']].max().max()], 
             'r--', alpha=0.5, label='Equal performance')
    # Add team labels
    for idx, row in df.iterrows():
        ax1.annotate(row['team'], (row['before_ppg_allowed'], row['after_ppg_allowed']), 
                    xytext=(3, 3), textcoords='offset points', fontsize=8, alpha=0.8)
    ax1.set_xlabel('Points Allowed Per Game (Before Bye)')
    ax1.set_ylabel('Points Allowed Per Game (After Bye)')
    ax1.set_title('Points Allowed Per Game')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Points allowed improvement by team
    df['ppg_allowed_improvement'] = df['before_ppg_allowed'] - df['after_ppg_allowed']  # Positive = improvement
    df_def_sorted = df.sort_values('ppg_allowed_improvement', ascending=True)
    colors = ['red' if x < 0 else 'green' for x in df_def_sorted['ppg_allowed_improvement']]
    bars = ax2.barh(range(len(df_def_sorted)), df_def_sorted['ppg_allowed_improvement'], color=colors, alpha=0.7)
    ax2.set_yticks(range(len(df_def_sorted)))
    ax2.set_yticklabels(df_def_sorted['team'], fontsize=8)
    ax2.set_xlabel('Change in Points Allowed Per Game')
    ax2.set_title('Defensive Improvement After Bye\n(Positive = Better Defense)')
    ax2.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, df_def_sorted['ppg_allowed_improvement'])):
        ax2.text(val + (0.2 if val >= 0 else -0.2), i, f'{val:+.1f}', 
                va='center', ha='left' if val >= 0 else 'right', fontsize=7)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

def create_detailed_team_table(pdf, df):
    """Create a detailed team statistics table"""
    fig = plt.figure(figsize=(11, 8.5))
    fig.suptitle('Detailed Team Statistics: Before vs After Bye Week', fontsize=14, fontweight='bold', y=0.95)
    
    # Select key columns for the table
    table_df = df[['team', 'bye_week', 'before_wins', 'before_losses', 'after_wins', 'after_losses',
                   'before_ppg_scored', 'after_ppg_scored', 'before_ppg_allowed', 'after_ppg_allowed']].copy()
    
    # Sort by team name
    table_df = table_df.sort_values('team')
    
    # Format the data for display
    table_data = []
    for _, row in table_df.iterrows():
        table_data.append([
            row['team'],
            f"Week {int(row['bye_week'])}",
            f"{int(row['before_wins'])}-{int(row['before_losses'])}",
            f"{int(row['after_wins'])}-{int(row['after_losses'])}",
            f"{row['before_ppg_scored']:.1f}",
            f"{row['after_ppg_scored']:.1f}",
            f"{row['before_ppg_allowed']:.1f}",
            f"{row['after_ppg_allowed']:.1f}"
        ])
    
    # Create table
    ax = fig.add_subplot(111)
    ax.axis('tight')
    ax.axis('off')
    
    headers = ['Team', 'Bye Week', 'W-L Before', 'W-L After', 
               'PPG Before', 'PPG After', 'PPA Before', 'PPA After']
    
    table = ax.table(cellText=table_data,
                    colLabels=headers,
                    cellLoc='center',
                    loc='center',
                    bbox=[0.05, 0.1, 0.9, 0.8])
    
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    table.scale(1, 1.5)
    
    # Style the table
    for i in range(len(table_data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            if i == 0:  # Header row
                cell.set_facecolor('#4472C4')
                cell.set_text_props(weight='bold', color='white')
            else:
                if i % 2 == 0:
                    cell.set_facecolor('#F8F8F8')
                else:
                    cell.set_facecolor('#FFFFFF')
    
    # Add legend
    plt.figtext(0.05, 0.05, "PPG = Points Per Game, PPA = Points Per Game Allowed", fontsize=8, style='italic')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

def main():
    """Main function to generate the PDF report"""
    print("Loading team performance data...")
    data = load_team_data()
    
    print("Processing data...")
    df = create_team_comparison_df(data)
    
    print(f"Creating PDF report for {len(df)} teams...")
    
    # Create PDF
    with PdfPages('nfl_2024_bye_week_analysis.pdf') as pdf:
        # Page 1: Summary statistics
        create_summary_stats_page(pdf, df)
        
        # Page 2: Offensive performance comparisons
        create_offense_comparison_charts(pdf, df)
        
        # Page 3: Team performance changes
        create_team_performance_charts(pdf, df)
        
        # Page 4: Defensive performance
        create_defensive_comparison_chart(pdf, df)
        
        # Page 5: Detailed team table
        create_detailed_team_table(pdf, df)
        
        # Set PDF metadata
        d = pdf.infodict()
        d['Title'] = "NFL 2024 Bye Week Performance Analysis"
        d['Author'] = "NFL Data Analysis"
        d['Subject'] = "Team performance comparison before and after bye weeks"
        d['Keywords'] = "NFL, 2024, Bye Week, Statistics, Performance"
        d['CreationDate'] = datetime.now()
    
    print("✅ PDF report generated successfully: nfl_2024_bye_week_analysis.pdf")
    print(f"📊 Analysis includes {len(df)} teams with complete before/after bye data")

if __name__ == "__main__":
    main()