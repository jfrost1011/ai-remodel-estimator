"""
Streamlit Cloud Entry Point for Renovation Cost Estimator

This file serves as the entry point for Streamlit Cloud deployment.
It sets up the necessary environment variables and launches the main application.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path to ensure imports work correctly
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# Set up environment variables for Streamlit Cloud
# In Streamlit Cloud, you'll set these in the app settings
# These are fallbacks for local development
os.environ.setdefault("EMBEDDING_MODEL_PATH", "jfrost10/renovation-cost-estimator-fine-tune")
os.environ.setdefault("MOCK_DATA", "true")  # Use mock data by default
os.environ.setdefault("USE_PINECONE", "false")
os.environ.setdefault("LOG_LEVEL", "INFO")

# Import and run the main application
from app import main

# Run the main function when this script is executed
if __name__ == "__main__":
    main() 