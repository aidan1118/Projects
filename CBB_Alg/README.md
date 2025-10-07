# College Basketball Prediction System

A comprehensive system for analyzing college basketball matchups and trends using the SportsData.io API. This system helps predict game outcomes and provides betting analysis.

## Features

- **Team Analysis**: Get detailed trends and statistics for any college basketball team
- **Matchup Analysis**: Compare two teams head-to-head with historical data
- **Betting Insights**: Analyze performance as favorites/underdogs and home/away trends
- **Data Export**: Save analysis to JSON, CSV, and PDF formats
- **Secure Configuration**: Environment-based API key management

## Setup

### Prerequisites
- Python 3.7+
- SportsData.io API key (college basketball subscription)

### Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API key:
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your SportsData.io API key
   SPORTSDATA_API_KEY=your_api_key_here
   ```

## Usage

The system provides both an interactive interface and command-line options:

### Interactive Interface (Recommended)
Run the interactive menu system:
```bash
python3 interactive.py
```

This provides a user-friendly menu with options to:
- Look up teams by name
- List all teams with pagination
- Get team trends & analysis
- Compare two teams (matchup analysis)
- Refresh team data from API
- View help & examples

### Command-Line Interface
For direct command usage:

#### List All Teams
```bash
python3 main.py --list-teams
```

#### Get Team Trends
```bash
python3 main.py --team-trends DUKE
python3 main.py --team-trends UNC
```

#### Analyze Team Matchup
```bash
python3 main.py --matchup DUKE UNC
python3 main.py --matchup GONZAGA BAYLOR
```

#### Advanced Options
```bash
# Verbose output
python3 main.py --matchup DUKE UNC -v

# Refresh teams data from API
python3 main.py --list-teams --refresh-teams

# Set log level
python3 main.py --team-trends DUKE --log-level DEBUG
```

## Project Structure

```
CBB_Alg/
├── interactive.py       # Interactive menu interface (recommended)
├── main.py              # CLI interface
├── config.py            # Configuration management
├── api_client.py        # SportsData.io API client
├── data_processor.py    # Data processing and analysis
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment file
├── .env                 # Your API configuration (not in git)
├── .gitignore           # Git ignore rules
├── data/                # Data storage directory
├── output/              # Output files directory
└── README.md           # This file
```

## API Endpoints Used

- **Teams Basic**: Get all team information
- **Team Trends**: Individual team performance trends
- **Matchup Trends**: Head-to-head historical data
- **Games**: Season game data
- **Player Stats**: Individual player statistics

## Data Analysis

The system analyzes several key factors:

### Team Performance
- Win/loss records overall and by context
- Average scoring (for and against)
- Performance as favorite vs underdog
- Home vs away performance

### Betting Analysis
- Point spread trends
- Over/under performance
- Situational betting patterns
- Historical matchup data

## Security

- API keys are stored in environment variables
- Sensitive files are excluded from version control
- Request logging for debugging without exposing credentials

## Output Files

The system generates several types of output:

- **CSV**: Team lists and basic statistics
- **JSON**: Detailed trend and analysis data
- **Logs**: System operation logs for debugging

## Legacy Files

The following files are from the original system and can be safely removed after migration:
- `team_data.py`
- `teams.py` 
- `teams_data.py`
- `test.py`
- `testy.py`

## Contributing

1. Ensure your API key is not committed to version control
2. Follow the existing code style and structure
3. Add logging for debugging purposes
4. Update documentation for new features

## Error Handling

The system includes comprehensive error handling for:
- Invalid team abbreviations
- API rate limits and timeouts
- Network connectivity issues
- Missing or corrupted data files

## Future Enhancements

- Web interface for easier usage
- Machine learning prediction models
- Real-time game monitoring
- Advanced betting strategy analysis
- Integration with multiple data sources