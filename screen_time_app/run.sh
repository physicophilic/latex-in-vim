#!/bin/bash
# Launcher script for Take Time Back screen time tracker

echo "Starting Take Time Back - Screen Time Tracker..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import psutil" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Run the application
python3 main.py
