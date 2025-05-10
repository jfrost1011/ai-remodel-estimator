@echo off
:: Renovation Cost Estimator Startup Script for Windows
:: This script handles startup of the application with proper error handling and fallbacks

echo 🔧 Starting Renovation Cost Estimator...

:: Check Python installation
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.8+ and try again.
    exit /b 1
)

:: Print Python version
echo 🐍 Using Python version:
python --version

:: Check for pip
pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ pip is not installed or not in PATH. Please install pip and try again.
    exit /b 1
)

:: Check if requirements.txt exists
if not exist requirements.txt (
    echo ⚠️ requirements.txt not found. Using minimal requirements...
    if exist minimal_requirements.txt (
        copy minimal_requirements.txt requirements.txt
    ) else (
        echo ❌ Neither requirements.txt nor minimal_requirements.txt found. Cannot continue.
        exit /b 1
    )
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo 🔧 Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo ❌ Failed to create virtual environment. Please install venv package and try again.
        exit /b 1
    )
)

:: Activate virtual environment
echo 🔧 Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ❌ Could not find activation script for virtual environment.
    exit /b 1
)

:: Upgrade pip
echo 🔧 Upgrading pip...
pip install --upgrade pip

:: Install requirements
echo 🔧 Installing requirements...
pip install -r requirements.txt
set INSTALL_RESULT=%ERRORLEVEL%

:: Check if requirements installation succeeded
if %INSTALL_RESULT% neq 0 (
    echo ⚠️ Full requirements installation failed. Trying minimal requirements...
    if exist minimal_requirements.txt (
        pip install -r minimal_requirements.txt
        if %ERRORLEVEL% neq 0 (
            echo ❌ Even minimal requirements installation failed. Cannot continue.
            exit /b 1
        )
    ) else (
        echo ❌ minimal_requirements.txt not found. Cannot continue.
        exit /b 1
    )
)

:: Set environment variables
set PYTHONPATH=%PYTHONPATH%;%CD%
set TOKENIZERS_PARALLELISM=false

:: Try to start the application
echo 🚀 Starting application...

:: Try full app first
if exist triple_fallback.py (
    echo 🔍 Using triple fallback system...
    streamlit run triple_fallback.py %*
) else if exist streamlit_app.py (
    echo 🔍 Using streamlit_app.py...
    streamlit run streamlit_app.py %*
) else if exist ultra_minimal_app.py (
    echo ⚠️ Falling back to ultra_minimal_app.py...
    streamlit run ultra_minimal_app.py %*
) else (
    echo ❌ Could not find any app entry point. Cannot continue.
    exit /b 1
) 