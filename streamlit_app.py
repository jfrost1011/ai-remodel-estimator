"""
Streamlit Cloud Entry Point for Renovation Cost Estimator

This file serves as the main entry point for Streamlit Cloud deployment.
It imports and runs the full functionality of the renovation estimator app.
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
renovation_dir = project_root / "renovation-estimator"
sys.path.append(str(renovation_dir))

# Print Python version for debugging
import platform
print(f"Python version: {platform.python_version()}")

# Set default environment variables
os.environ.setdefault("EMBEDDING_MODEL_PATH", "text-embedding-3-small")
os.environ.setdefault("MOCK_DATA", "true")
os.environ.setdefault("USE_PINECONE", "false")
os.environ.setdefault("LOG_LEVEL", "INFO")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")  # Prevents warnings

# Import and run the app
try:
    print("Importing app module...")
    sys.path.insert(0, str(renovation_dir))
    from app import main
    print("Successfully imported app module")
except ImportError as e:
    print(f"Error importing app module: {e}")
    print("Available modules in path:")
    for p in sys.path:
        print(f"  - {p}")
    
    print("Searching for app.py...")
    import glob
    for path in glob.glob("**/*.py", recursive=True):
        if "app.py" in path:
            print(f"Found: {path}")

# If running this file directly
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"Error running main: {e}")
        traceback.print_exc() 