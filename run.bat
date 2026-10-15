@echo off
cd /d "%~dp0"
echo Starting My Personal AI Teacher...
where py >nul 2>nul
if %errorlevel%==0 (
  py server.py
) else (
  python server.py
)
if errorlevel 1 (
  echo.
  echo Could not start. Install Python 3 from https://www.python.org/downloads/
  echo During installation, tick "Add Python to PATH".
  pause
)
