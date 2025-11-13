@echo off
echo 🏈 Starting NFL Data API...

REM Detect Python command
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=python
) else (
    python3 --version >nul 2>&1
    if %errorlevel%==0 (
        set PYTHON_CMD=python3
    ) else (
        echo ❌ Python not found. Please install Python 3.7+
        pause
        exit /b 1
    )
)

REM Detect pip command  
set PIP_CMD=
pip --version >nul 2>&1
if %errorlevel%==0 (
    set PIP_CMD=pip
) else (
    pip3 --version >nul 2>&1
    if %errorlevel%==0 (
        set PIP_CMD=pip3
    ) else (
        echo ❌ pip not found. Please install pip
        pause
        exit /b 1
    )
)

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Creating one...
    %PYTHON_CMD% -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment  
echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

REM Update commands to use venv versions
if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD=venv\Scripts\python.exe
    set PIP_CMD=venv\Scripts\pip.exe
)

REM Install/update requirements
echo ⬇️  Installing dependencies...
%PIP_CMD% install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Check for existing processes on port 5001
echo 🔄 Checking for existing server...
netstat -an | findstr :5001 >nul 2>&1
if %errorlevel%==0 (
    echo ⚠️  Port 5001 appears to be in use. You may need to stop existing processes manually.
    echo    You can use: taskkill /f /im python.exe
)

REM Start the server
echo 🚀 Starting NFL API on http://localhost:5001
echo 📊 Available endpoints:
echo    • http://localhost:5001/ (API info)
echo    • http://localhost:5001/nfl/games
echo    • http://localhost:5001/nfl/stats
echo    • http://localhost:5001/nfl/teams
echo    • http://localhost:5001/nfl/bye-weeks
echo    • http://localhost:5001/nfl/team-performance
echo.
echo Press Ctrl+C to stop the server
echo ================================

REM Run the app
%PYTHON_CMD% app.py