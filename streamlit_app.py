"""
Streamlit Cloud Entry Point for Renovation Cost Estimator

This file serves as the main entry point for Streamlit Cloud deployment.
It imports and runs the full functionality of the renovation estimator app.
If dependencies are missing, it falls back to a simplified version.
"""
import os
import sys
from pathlib import Path
import traceback

# Print Python version for debugging
import platform
print(f"Python version: {platform.python_version()}")

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
renovation_dir = project_root / "renovation-estimator"
sys.path.append(str(renovation_dir))
sys.path.append(str(project_root))

# Set default environment variables
os.environ.setdefault("EMBEDDING_MODEL_PATH", "text-embedding-3-small")
os.environ.setdefault("MOCK_DATA", "true")
os.environ.setdefault("USE_PINECONE", "false")
os.environ.setdefault("LOG_LEVEL", "INFO")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")  # Prevents warnings

# Import streamlit for the fallback app
import streamlit as st

def run_full_app():
    """Try to run the full app with all features."""
    try:
        print("Importing app module...")
        sys.path.insert(0, str(renovation_dir))
        from app import main
        print("Successfully imported app module")
        return main
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
        return None

def run_cloud_app():
    """Run the simplified cloud app."""
    try:
        print("Trying to import cloud_app...")
        import cloud_app
        print("Successfully imported cloud_app")
        return True
    except ImportError as e:
        print(f"Error importing cloud_app: {e}")
        return False

def run_fallback_app():
    """Run an extremely simple app directly in this file."""
    print("Running fallback app directly")
    
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Set up the page
    st.set_page_config(
        page_title="Renovation Cost Estimator",
        page_icon="🏠",
        layout="wide"
    )
    
    # Main app header
    st.title("🏠 Renovation Cost Estimator")
    st.subheader("Fallback Version")
    
    st.warning("""
    This is a simplified fallback version of the Renovation Cost Estimator.
    The full version couldn't be loaded due to dependency issues.
    """)
    
    st.markdown("""
    The complete version includes:
    - Cost estimation based on project details
    - Semantic search for similar projects
    - Visualization of cost breakdowns
    - PDF report generation
    """)
    
    # Sample data for demonstration
    sample_projects = [
        {"type": "Kitchen", "size": 200, "grade": "Premium", "cost": 45000},
        {"type": "Bathroom", "size": 100, "grade": "Standard", "cost": 25000},
        {"type": "Addition", "size": 400, "grade": "Luxury", "cost": 150000}
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(sample_projects)
    
    # Display sample data
    st.subheader("Sample Renovation Projects")
    st.dataframe(df)
    
    # Simple interactive elements
    st.subheader("Try a Simple Estimate")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_type = st.selectbox("Project Type", ["Kitchen", "Bathroom", "Addition"])
        square_feet = st.slider("Square Footage", 50, 1000, 200)
    
    with col2:
        material_grade = st.radio("Material Grade", ["Standard", "Premium", "Luxury"])
    
    # Simple calculation for demo
    base_costs = {
        "Kitchen": 200,
        "Bathroom": 250,
        "Addition": 300
    }
    
    multipliers = {
        "Standard": 1.0,
        "Premium": 1.5,
        "Luxury": 2.2
    }
    
    # Calculate estimated cost
    base_cost = base_costs.get(project_type, 200)
    multiplier = multipliers.get(material_grade, 1.0)
    estimated_cost = base_cost * square_feet * multiplier
    
    # Display result
    st.subheader("Estimated Cost")
    st.metric("Total Cost", f"${int(estimated_cost):,}")
    
    # Create a simple chart
    st.subheader("Cost Breakdown")
    fig, ax = plt.subplots()
    breakdown = {
        "Materials": 0.4 * estimated_cost,
        "Labor": 0.35 * estimated_cost,
        "Permits": 0.1 * estimated_cost,
        "Design": 0.15 * estimated_cost
    }
    
    ax.bar(breakdown.keys(), breakdown.values())
    ax.set_ylabel("Cost ($)")
    ax.set_title("Cost Breakdown")
    for i, v in enumerate(breakdown.values()):
        ax.text(i, v + 1000, f"${int(v):,}", ha='center')
    
    st.pyplot(fig)
    
    # Footer
    st.markdown("---")
    st.caption("© 2024 Renovation Estimator - Fallback Version")

# If running this file directly
if __name__ == "__main__":
    try:
        # Try to run the full app
        main_func = run_full_app()
        if main_func:
            main_func()
        # If that fails, try the cloud app
        elif run_cloud_app():
            pass  # cloud_app already runs when imported
        # If that also fails, run the built-in fallback
        else:
            run_fallback_app()
    except Exception as e:
        print(f"Error running app: {e}")
        traceback.print_exc()
        st.error(f"Error loading the application: {e}")
        run_fallback_app() 