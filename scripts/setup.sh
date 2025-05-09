#!/bin/bash

# Setup script for Renovation Estimator project
# Uses uv for faster Python environment setup

echo "Setting up Renovation Estimator environment..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Installing uv package manager..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        curl --proto '=https' --tlsv1.2 -LsSf https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh | sh
    else
        # Linux or Windows (WSL)
        curl -LsSf https://astral.sh/uv/install.sh | bash
    fi
    echo "uv installed successfully!"
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Install dependencies
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Create necessary data directories
mkdir -p data/synthetic
mkdir -p data/fine_tuning
mkdir -p data/evaluation

echo "Environment setup complete!"
echo "To activate the environment, run: source .venv/bin/activate (Linux/macOS) or .venv\\Scripts\\activate (Windows)"
echo "To run the application, run: streamlit run app.py" 