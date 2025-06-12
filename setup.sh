#!/bin/bash
echo "--- AI Photo Organizer Setup for macOS/Linux ---"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed. Please install it before running this script."
    exit 1
fi

echo "Step 1: Creating a Python virtual environment..."
python3 -m venv venv

# Check if virtual environment was created successfully
if [ ! -d "venv" ]; then
    echo "ERROR: Failed to create the virtual environment."
    exit 1
fi

echo "Step 2: Activating the environment and installing required packages..."
# Activate the environment and run pip install in a subshell
(
    source venv/bin/activate
    pip install -r requirements.txt
)

echo ""
echo "--- SETUP COMPLETE ---"
echo "You can now enroll faces and run the organizer."
echo "To run the enrollment script, use: ./run.sh enroll"
echo "To run the main organizer, use:   ./run.sh organize"