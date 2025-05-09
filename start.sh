#!/bin/bash

echo "Starting Renovation Estimator..."

# Check if the virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment and installing dependencies..."
    echo "This may take a few minutes..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if data exists
if [ ! -f "data/synthetic/sample_projects.json" ]; then
    echo "Generating sample data..."
    python scripts/generate_data.py
fi

# Start the app
echo "Starting Streamlit app..."
streamlit run app.py 