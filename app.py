"""
Root-level Streamlit app entry point.
This file serves as the entry point for Streamlit Cloud and imports the actual app
from the renovation-estimator directory.
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
renovation_dir = project_root / "renovation-estimator"
sys.path.append(str(renovation_dir))

# Set default environment variables
os.environ.setdefault("EMBEDDING_MODEL_PATH", "jfrost10/renovation-cost-estimator-fine-tune")
os.environ.setdefault("MOCK_DATA", "true")
os.environ.setdefault("USE_PINECONE", "false")
os.environ.setdefault("LOG_LEVEL", "INFO")

# Import the main function from the renovation-estimator app
import importlib.util
spec = importlib.util.spec_from_file_location("app", str(renovation_dir / "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)
main = app_module.main

# Run the main function when this script is executed
if __name__ == "__main__":
    main() 