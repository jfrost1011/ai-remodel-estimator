"""
Streamlit Cloud Entry Point

This file serves as the main entry point for Streamlit Cloud deployment.
It imports and runs the cloud app to avoid dependency conflicts.
"""
import platform
print(f"Python version: {platform.python_version()}")

# Import the cloud app
from cloud_app import *

# If running this file directly
if __name__ == "__main__":
    # The cloud_app.py content will be executed due to the import
    pass 