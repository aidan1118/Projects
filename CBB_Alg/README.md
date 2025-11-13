# College Basketball Analyzing System

> **Data Quality Disclaimer**: This system uses the free tier of the SportsData.io API, which has significant data quality issues including:
> - **Inflated/Unrealistic Scores**: Average scores often appear as 140-160 points per game (normal college basketball averages 65-85)
> - **Inconsistent Data**: Different API endpoints return conflicting information for the same teams
> - **Limited Accuracy**: Free-tier data may be delayed, incomplete, or contain calculation errors
> 
> **Important**: The analytical methods, data processing logic, and calculations implemented in this system are accurate and production-ready. The issues stem from the underlying API data quality, not the processing algorithms. When connected to premium/accurate data sources, this system would produce reliable analysis.
>
> **Project Status**: This is an early-stage version of the system. Future development plans include upgrading to a premium API with accurate data, enhancing analytical capabilities, and expanding features. The current version serves as a demonstration of the analytical framework and processing methods.

A comprehensive system for analyzing college basketball matchups and trends using the SportsData.io API. This system provides clean, data-driven analysis for current season team performance and head-to-head comparisons.

## Features

- **Team Lookup & Search**: Search teams by name, location, or abbreviation
- **Current Season Team Analysis**: Get detailed trends and statistics with accurate game counts
- **Matchup Analysis**: Compare two teams head-to-head with historical data and performance metrics
- **PDF Reports**: Comprehensive PDF reports with detailed shooting, scoring, and performance breakdowns
- **Clean Interface**: Streamlined user interface without distracting elements
- **Secure Configuration**: Environment-based API key management

## Setup

### Prerequisites
- Python 3.7+

### Installation

1. Clone or download the project
2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ready to use!** The system includes a free-tier API key for immediate use. No additional setup required.

### Using Your Own API Key (Optional)

If you have your own SportsData.io API key for potentially better rate limits, simply set the environment variable:
```bash
export SPORTSDATA_API_KEY=your_api_key_here
```

## Usage

### Interactive Interface (Primary Method)
Run the interactive menu system:
```bash
python3 interactive.py
```

This provides a user-friendly menu with options to:
- **Team Lookup**: Search teams by name, location, or abbreviation
- **List All Teams**: Browse all available teams with pagination
- **Team Trends Analysis**: Get current season performance data with accurate game counts
- **Matchup Analysis**: Sequential team selection for head-to-head comparison
- **Data Refresh**: Update team information from the API
- **Help & Examples**: Usage guidance and common team abbreviations

### Key Features

#### Team Search and Selection
- Search by partial names: "duke", "carolina", "state"
- Use exact abbreviations: "DUKE", "NCAR", "GONZ"
- Sequential team selection for matchup analysis

#### Current Season Data
- Accurate game counts (fixes API data inconsistencies)
- Recent performance trends (Last 3, 5, 10 games)
- Upcoming game information
- Performance metrics and averages

#### PDF Reports
All analysis is automatically saved as detailed PDF reports in the `data/` directory:
- **Team Analysis**: Performance tables, upcoming games, recent trends
- **Matchup Analysis**: Head-to-head history, detailed performance breakdowns, key factors

## Project Structure

```
CBB_Alg/
├── interactive.py       # Interactive menu interface (main entry point)
├── config.py            # Configuration management  
├── api_client.py        # SportsData.io API client
├── data_processor.py    # Data processing and analysis with scope fixes
├── utils.py             # Utility functions and PDF generation
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment file with public API key
├── .env                 # API configuration (tracked - contains public key)
├── .gitignore           # Git ignore rules
├── data/                # Data storage and PDF output directory
│   └── teams_info.csv   # Team information cache
└── README.md           # This file
```

## API Endpoints Used

- **Teams Basic**: Get all team information and maintain local cache
- **Team Trends**: Current season team performance trends with scope correction
- **Matchup Trends**: Head-to-head historical data and previous games

## Data Analysis

The system provides clean, current-season analysis:

### Team Performance Analysis
- Win/loss records with accurate game counts
- Average scoring (for and against) 
- Recent performance trends (Last 3, 5, 10 games)
- Point differential calculations
- Upcoming game information

### Matchup Analysis
- Head-to-head historical performance
- Detailed performance breakdowns for both teams
- Recent game history with scores and winners
- Performance metrics comparison
- Key factors for analysis

## Output Files

The system generates the following outputs:

- **CSV**: `teams_info.csv` - Cached team information (TeamID, Key, School, Name, Conference)
- **PDF**: Detailed analysis reports saved to `data/` directory
  - Team trends: `team_trends_{TEAM}_{timestamp}.pdf`
  - Matchup analysis: `matchup_analysis_{TEAM1}_vs_{TEAM2}_{timestamp}.pdf`
- **Logs**: System operation logs (`cbb_prediction.log`)

## Security

- Uses free-tier public API key for easy demo access
- Optional environment variable override for custom API keys  
- Sensitive files excluded from version control (logs, custom .env files)
- Clean data processing without exposing user credentials

## Error Handling

The system includes robust error handling for:
- Invalid team abbreviations with search suggestions
- API rate limits and network issues
- Data scope corrections for accurate game counts
- Graceful fallbacks for missing data

## Team Abbreviation Examples

Common team abbreviations for quick reference:
- Duke: `DUKE`
- North Carolina: `NCAR` 
- Kentucky: `UK`
- Kansas: `KU`
- Gonzaga: `GONZ`
- Villanova: `NOVA`
- UCLA: `UCLA`
- Michigan: `MICH`

Use the team lookup feature to find any team's abbreviation.