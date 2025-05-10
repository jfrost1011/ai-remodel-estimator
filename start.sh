#!/bin/bash
# Renovation Cost Estimator Startup Script
# This script handles startup of the application with proper error handling and fallbacks

echo "🔧 Starting Renovation Cost Estimator..."

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check Python installation
if ! command_exists python3; then
  echo "❌ Python 3 is not installed or not in PATH. Please install Python 3.8+ and try again."
  exit 1
fi

# Print Python version
PYTHON_VERSION=$(python3 --version)
echo "🐍 Using $PYTHON_VERSION"

# Check for pip
if ! command_exists pip3; then
  echo "❌ pip3 is not installed or not in PATH. Please install pip and try again."
  exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
  echo "⚠️ requirements.txt not found. Using minimal requirements..."
  if [ -f "minimal_requirements.txt" ]; then
    cp minimal_requirements.txt requirements.txt
  else
    echo "❌ Neither requirements.txt nor minimal_requirements.txt found. Cannot continue."
    exit 1
  fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "🔧 Creating virtual environment..."
  python3 -m venv venv
  if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment. Please install venv package and try again."
    exit 1
  fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
  source venv/Scripts/activate
else
  echo "❌ Could not find activation script for virtual environment."
  exit 1
fi

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "🔧 Installing requirements..."
pip install -r requirements.txt
INSTALL_RESULT=$?

# Check if requirements installation succeeded
if [ $INSTALL_RESULT -ne 0 ]; then
  echo "⚠️ Full requirements installation failed. Trying minimal requirements..."
  if [ -f "minimal_requirements.txt" ]; then
    pip install -r minimal_requirements.txt
    if [ $? -ne 0 ]; then
      echo "❌ Even minimal requirements installation failed. Cannot continue."
      exit 1
    fi
  else
    echo "❌ minimal_requirements.txt not found. Cannot continue."
    exit 1
  fi
fi

# Set environment variables
export PYTHONPATH="$PYTHONPATH:$(pwd)"
export TOKENIZERS_PARALLELISM="false"

# Try to start the application
echo "🚀 Starting application..."

# Try full app first
if [ -f "triple_fallback.py" ]; then
  echo "🔍 Using triple fallback system..."
  streamlit run triple_fallback.py "$@"
elif [ -f "streamlit_app.py" ]; then
  echo "🔍 Using streamlit_app.py..."
  streamlit run streamlit_app.py "$@"
elif [ -f "ultra_minimal_app.py" ]; then
  echo "⚠️ Falling back to ultra_minimal_app.py..."
  streamlit run ultra_minimal_app.py "$@"
else
  echo "❌ Could not find any app entry point. Cannot continue."
  exit 1
fi 