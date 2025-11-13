# NFL Analytics Platform

A comprehensive NFL data analysis platform that combines a robust REST API with advanced reporting capabilities. Built with Python/Flask and data visualization libraries, this platform provides real-time NFL statistics, automated report generation, and seamless Power BI integration.

## Key Features

### **REST API** 
- **Real-time NFL Data**: Live game scores, player statistics, and team information
- **Power BI Integration**: JSON endpoints with CORS support for dashboard creation
- **Flexible Querying**: Filter by year, week, team, and statistical categories
- **Comprehensive Coverage**: All 32 teams, full season data, bye week analysis

### **Automated Report Generation**
- **Professional PDF Reports**: League-wide bye week performance analysis with charts and visualizations
- **Team-Specific Reports**: Detailed HTML/PDF reports for individual team analysis
- **Statistical Visualizations**: Matplotlib and Seaborn charts for data insights
- **Export Capabilities**: Multiple output formats (PDF, HTML, JSON, CSV)

### **Data Analysis**
- **Before/After Bye Week Comparisons**: Team performance analysis with statistical significance
- **Offensive & Defensive Metrics**: Points, yards, touchdowns, win/loss records
- **Performance Trending**: Identify teams that improve or decline after rest periods
- **League Benchmarking**: Compare individual team performance against league averages

## Quick Start

### Prerequisites
- Python 3.7+ (Python 3.8+ recommended)
- Virtual environment (strongly recommended)
- Internet connection for NFL data fetching

### Installation

```bash
# Clone and navigate to project
git clone <repository-url>
cd nfl-api

# Set up virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate    # Mac/Linux
# or
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

### Launch Options

#### **Option 1: Quick Start (Recommended)**
```bash
# Make scripts executable (Mac/Linux only)
chmod +x start.sh test_api.sh generate_team_pdf.py

# Start the API server
./start.sh        # Mac/Linux
start.bat         # Windows
```

#### **Option 2: Manual Launch**
```bash
# Activate virtual environment
source venv/bin/activate    # Mac/Linux
# or
venv\Scripts\activate       # Windows

# Start the Flask API server
python app.py
```

The API will be available at `http://localhost:5001`

### Verify Installation
```bash
# Test the API endpoints
./test_api.sh

# Or manually test
curl http://localhost:5001/
```

## Usage Guide

### **Step 1: Start the API Server**

The API server must be running for most operations:

```bash
# Terminal 1: Start the API
source venv/bin/activate
python app.py

# You should see:
# * Running on http://127.0.0.1:5001
# * Debug mode: on
```

**Troubleshooting API Startup:**
- **Port in use**: Change port in `app.py` (line with `app.run(port=5001)`)
- **Module errors**: Ensure `pip install -r requirements.txt` completed successfully
- **Network issues**: Check internet connection for NFL data fetching

### **Step 2: Generate Reports**

With the API running, open a new terminal:

```bash
# Terminal 2: Generate reports
source venv/bin/activate

# List all available teams
python generate_team_pdf.py --list-teams

# Generate individual team report
python generate_team_pdf.py BUF    # Buffalo Bills

# Generate with specific year
python generate_team_pdf.py KC --year 2024    # Kansas City Chiefs 2024
```

### **Step 3: Export Data for Analysis**

```bash
# Generate league-wide PDF analysis
python create_bye_week_pdf.py

# Export to CSV for Power BI/Excel
python export_to_csv.py
```

## Report Generation

### Generate League-Wide Analysis Report

**Purpose**: Comprehensive analysis of all 32 NFL teams' bye week performance

```bash
# Ensure API is running first
python app.py &

# Generate the report (in new terminal)
source venv/bin/activate
python create_bye_week_pdf.py
```

**Output**: `nfl_2024_bye_week_analysis.pdf`

**Report Contents**:
- Executive summary with league-wide statistics
- Teams showing improvement after bye weeks
- Teams showing decline after bye weeks  
- Offensive performance comparisons (points, rushing, passing)
- Defensive analysis and trends
- Detailed team-by-team statistics table
- Visual charts and graphs

### Generate Individual Team PDF Reports

**Purpose**: Deep-dive analysis of any specific NFL team

```bash
# Start API server first (if not already running)
python app.py &

# Generate PDF report for any team
python generate_team_pdf.py <TEAM_CODE> [--year YYYY]

# Examples:
python generate_team_pdf.py BUF    # Buffalo Bills 
python generate_team_pdf.py KC     # Kansas City Chiefs
python generate_team_pdf.py SF     # San Francisco 49ers
python generate_team_pdf.py DAL --year 2023    # Dallas Cowboys 2023

# List all available team codes
python generate_team_pdf.py --list-teams
```

**Output Files**:
- `{team}_{year}_report.pdf` - Professional PDF with charts and analysis
- `{team}_{year}_data.json` - Raw data in JSON format

### Export Data to CSV for Business Intelligence

**Purpose**: Create Power BI/Excel-ready datasets

```bash
# Export team performance data to CSV
python export_to_csv.py
```

**Output**: `nfl_team_performance.csv`

**Power BI Import Steps**:
1. Open Power BI Desktop
2. **Get Data** → **Text/CSV**
3. Select `nfl_team_performance.csv`
4. **Transform Data** → Verify data types
5. **Close & Apply** to load data

## NFL Team Codes Reference

### AFC Conference

#### AFC East
| Code | Team Name |
|------|-----------|
| `BUF` | Buffalo Bills |
| `MIA` | Miami Dolphins |
| `NE` | New England Patriots |
| `NYJ` | New York Jets |

#### AFC North  
| Code | Team Name |
|------|-----------|
| `BAL` | Baltimore Ravens |
| `CIN` | Cincinnati Bengals |
| `CLE` | Cleveland Browns |
| `PIT` | Pittsburgh Steelers |

#### AFC South
| Code | Team Name |
|------|-----------|
| `HOU` | Houston Texans |
| `IND` | Indianapolis Colts |
| `JAX` | Jacksonville Jaguars |
| `TEN` | Tennessee Titans |

#### AFC West
| Code | Team Name |
|------|-----------|
| `DEN` | Denver Broncos |
| `KC` | Kansas City Chiefs |
| `LAC` | Los Angeles Chargers |
| `LV` | Las Vegas Raiders |

### NFC Conference

#### NFC East
| Code | Team Name |
|------|-----------|
| `DAL` | Dallas Cowboys |
| `NYG` | New York Giants |
| `PHI` | Philadelphia Eagles |
| `WAS` | Washington Commanders |

#### NFC North
| Code | Team Name |
|------|-----------|
| `CHI` | Chicago Bears |
| `DET` | Detroit Lions |
| `GB` | Green Bay Packers |
| `MIN` | Minnesota Vikings |

#### NFC South
| Code | Team Name |
|------|-----------|
| `ATL` | Atlanta Falcons |
| `CAR` | Carolina Panthers |
| `NO` | New Orleans Saints |
| `TB` | Tampa Bay Buccaneers |

#### NFC West
| Code | Team Name |
|------|-----------|
| `ARI` | Arizona Cardinals |
| `LA` | Los Angeles Rams |
| `SF` | San Francisco 49ers |
| `SEA` | Seattle Seahawks |



## API Documentation

### Core Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/` | GET | API documentation and health check | None |
| `/nfl/games` | GET | Game schedules and results | `year`, `week` |
| `/nfl/stats` | GET | Player statistics | `year`, `type` |
| `/nfl/teams` | GET | Team information and metadata | None |
| `/nfl/bye-weeks` | GET | Bye week schedules | `year` |
| `/nfl/team-performance` | GET | Before/after bye week analysis | `year`, `team` |

### API Usage Examples

```bash
# Get API information
curl "http://localhost:5001/"

# Get all 2024 bye weeks
curl "http://localhost:5001/nfl/bye-weeks?year=2024"

# Get Buffalo Bills performance analysis
curl "http://localhost:5001/nfl/team-performance?team=BUF&year=2024"

# Get Week 1 games for 2024
curl "http://localhost:5001/nfl/games?year=2024&week=1"

# Get all team information
curl "http://localhost:5001/nfl/teams"
```

### Sample API Response

```json
{
  "data": [
    {
      "season": 2024,
      "team": "BUF",
      "bye_week": 12,
      "period": "before_bye",
      "games_played": 11,
      "total_points_scored": 320,
      "avg_points_scored": 29.09,
      "total_points_allowed": 214,
      "avg_points_allowed": 19.45,
      "wins": 9,
      "losses": 2,
      "home_games": 5,
      "away_games": 6,
      "total_passing_yards": 2548.0,
      "avg_passing_yards": 231.64,
      "total_rushing_yards": 1311.0,
      "avg_rushing_yards": 119.18
    }
  ],
  "count": 1
}
```

## Power BI Integration

### Method 1: Direct API Connection (Real-time)

1. **Start the API Server**:
   ```bash
   python app.py
   ```

2. **Open Power BI Desktop**

3. **Get Data** → **Web** → Enter API URL:
   ```
   http://localhost:5001/nfl/team-performance?year=2024
   ```

4. **Transform Data**:
   - Expand the "data" column
   - Set appropriate data types
   - Rename columns as needed

5. **Load Data** → **Close & Apply**

### Method 2: CSV Import (Static snapshot)

1. **Export Data to CSV**:
   ```bash
   python export_to_csv.py
   ```

2. **Power BI Import**:
   - **Get Data** → **Text/CSV**
   - Select `nfl_team_performance.csv`
   - **Load**

### Recommended Power BI URLs
```
http://localhost:5001/nfl/team-performance?year=2024
http://localhost:5001/nfl/bye-weeks?year=2024
http://localhost:5001/nfl/teams
http://localhost:5001/nfl/games?year=2024
```

## Technical Architecture

### Technology Stack
- **Backend**: Python 3.7+, Flask 3.0+
- **Data Processing**: Pandas 2.2+, NumPy
- **Data Source**: nfl-data-py library (official NFL statistics)
- **Visualization**: Matplotlib 3.7+, Seaborn 0.12+
- **PDF Generation**: ReportLab, Matplotlib backends
- **API Features**: Flask-CORS, JSON responses, error handling
- **Export Formats**: PDF, JSON, CSV

### Project Structure
```
nfl-api/
├── app.py                          # Flask API server (main entry point)
├── create_bye_week_pdf.py          # League-wide PDF report generator
├── generate_team_pdf.py            # Team-specific PDF report generator  
├── export_to_csv.py                # CSV export utility for Power BI
├── requirements.txt                # Python dependencies
├── team_performance.json           # Cached performance data
├── test_api.sh                     # API testing script
├── start.sh / start.bat           # Cross-platform startup scripts
├── venv/                           # Virtual environment (created during setup)
├── *.pdf                          # Generated reports
├── *.json                         # Generated data exports
├── *.csv                          # Generated CSV files
└── README.md                      # This documentation
```

## Testing & Troubleshooting

### Automated Testing
```bash
# Run comprehensive API tests
./test_api.sh

# Expected output: JSON responses for all endpoints
```

### Common Issues & Solutions

#### **"Module not found" errors**
```bash
# Solution: Activate virtual environment and reinstall
source venv/bin/activate
pip install -r requirements.txt
```

#### **"Port 5001 already in use"**
```bash
# Solution 1: Kill existing process
pkill -f "python.*app.py"

# Solution 2: Use different port (edit app.py)
# Change: app.run(port=5001) to app.run(port=5002)
```

#### **"Connection refused" when generating reports**
```bash
# Solution: Start API server first
python app.py &
# Then run report generation in new terminal
python generate_team_pdf.py BUF
```

#### **Empty or incomplete reports**
- **Cause**: API server not running or network issues
- **Solution**: Ensure API server is running and internet connection is stable
- **Verification**: Test with `curl http://localhost:5001/`

#### **"No data for team X"**
- **Cause**: Invalid team code or season
- **Solution**: Use `python generate_team_pdf.py --list-teams` for valid codes
- **Note**: Some historical seasons may have limited data

### Test Data Validation
```bash
# Validate team performance data
python -c "
import json
with open('team_performance.json', 'r') as f:
    data = json.load(f)
    print(f'Teams: {len(set([team[\"team\"] for team in data]))}')
    print(f'Records: {len(data)}')
    print(f'Seasons: {set([team[\"season\"] for team in data])}')
"
```

## Data Sources & Attribution

### Primary Data Source
**nfl-data-py Library**
- **GitHub**: https://github.com/cooperdff/nfl_data_py
- **Documentation**: https://github.com/cooperdff/nfl_data_py/blob/master/README.md
- **Data Coverage**: 1999-present NFL seasons
- **Update Frequency**: Weekly during NFL season
- **Data Types**: Games, player stats, team info, rosters, draft data


---

*This NFL Analytics Platform demonstrates comprehensive full-stack development skills including REST API design, data processing, statistical analysis, automated reporting, business intelligence integration, and professional documentation.*