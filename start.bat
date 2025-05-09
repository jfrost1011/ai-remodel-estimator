@echo off
echo Starting Renovation Estimator...

REM Check if the virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment and installing dependencies...
    echo This may take a few minutes...
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r requirements.txt
) else (
    echo Activating virtual environment...
    call .venv\Scripts\activate
)

REM Check if data exists
if not exist "data\synthetic\sample_projects.json" (
    echo Generating sample data...
    python scripts\generate_data.py
)

REM Start the app
echo Starting Streamlit app...
streamlit run app.py

pause 