#!/bin/bash
# Activate the virtual environment
source venv/bin/activate

if [ "$1" == "enroll" ]; then
    echo "--- Starting Face Enrollment ---"
    python3 enroll_faces.py
elif [ "$1" == "organize" ]; then
    echo "--- Starting Photo Organizer ---"
    python3 photo_organizer.py
else
    echo "Usage: ./run.sh [enroll|organize]"
fi