@echo off
REM Activate the virtual environment
call venv\Scripts\activate.bat

if "%1"=="enroll" (
    ECHO --- Starting Face Enrollment ---
    py -3 enroll_faces.py
) else if "%1"=="organize" (
    ECHO --- Starting Photo Organizer ---
    py -3 photo_organizer.py
) else (
    ECHO Usage: run.bat [enroll^|organize]
)
pause