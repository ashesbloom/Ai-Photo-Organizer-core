@echo off
ECHO --- AI Photo Organizer Setup for Windows ---

REM Check if Python is installed and available
py -3 --version >nul 2>nul
if %errorlevel% neq 0 (
    ECHO ERROR: Python 3 is not found. Please install it and add it to your PATH.
    pause
    exit /b 1
)

ECHO Step 1: Creating a Python virtual environment...
py -3 -m venv venv

IF NOT EXIST "venv\Scripts\activate.bat" (
    ECHO ERROR: Failed to create the virtual environment.
    pause
    exit /b 1
)

ECHO Step 2: Activating the environment and installing required packages...
call venv\Scripts\activate.bat
pip install -r requirements.txt

ECHO.
ECHO --- SETUP COMPLETE ---
ECHO You can now enroll faces and run the organizer.
ECHO To run the enrollment script, use: run.bat enroll
ECHO To run the main organizer, use:   run.bat organize
pause