"""
Renovation Cost Estimator Application

This is the main Streamlit application for the Renovation Cost Estimator.
"""

import streamlit as st

# 🔹 FIRST Streamlit command on the page 🔹
st.set_page_config(
    page_title="Renovation Cost Estimator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
import sys
from pathlib import Path

# Add the current directory to Python path to ensure imports work correctly
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# Import dependencies
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
import logging
log_level = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Set default environment variables for the app
os.environ.setdefault("EMBEDDING_MODEL_PATH", "jfrost10/renovation-cost-estimator-fine-tune")
os.environ.setdefault("MOCK_DATA", "true")
os.environ.setdefault("USE_PINECONE", "false")

# Try-except blocks for imports to handle potential import errors gracefully
try:
    # Import backend modules
    from backend import get_cost_estimate, search_similar_projects
    from backend.data_generator import generate_sample_data
    from utils.data_loader import load_sample_data
except ImportError as e:
    logger.error(f"Error importing backend modules: {e}")
    st.error(f"Failed to load backend modules: {e}")

try:
    # Import UI components
    from ui import render_home_page, render_estimate_page, render_search_page, render_dashboard_page, render_admin_page
except ImportError as e:
    logger.error(f"Error importing UI components: {e}")
    st.error(f"Failed to load UI components: {e}")

# Define the main function
def main():
    """Main application function that handles page rendering."""
    try:
        # Save selected page in session state for navigation between pages
        if "sidebar_selection" not in st.session_state:
            st.session_state.sidebar_selection = "Home"
            
        # Create sidebar for navigation
        with st.sidebar:
            st.title("🏠 Renovation Estimator")
            st.markdown("---")
            
            # Navigation options
            selected_page = st.radio(
                "Navigate to:",
                ["Home", "Cost Estimator", "Smart Search", "Dashboard", "Admin"],
                index=["Home", "Cost Estimator", "Smart Search", "Dashboard", "Admin"].index(st.session_state.sidebar_selection)
            )
            
            # Update session state
            st.session_state.sidebar_selection = selected_page
            
            st.markdown("---")
            st.caption("© 2024 Renovation Estimator")
            
        # Render the selected page
        try:
            if selected_page == "Home":
                render_home_page()
            elif selected_page == "Cost Estimator":
                render_estimate_page()
            elif selected_page == "Smart Search":
                render_search_page()
            elif selected_page == "Dashboard":
                render_dashboard_page()
            elif selected_page == "Admin":
                render_admin_page()
        except Exception as e:
            logger.error(f"Error rendering page {selected_page}: {e}")
            st.error(f"Error loading page: {e}")
            st.info("Try restarting the application or contact support if the issue persists.")
    except Exception as e:
        logger.error(f"Critical application error: {e}")
        st.error("The application encountered a critical error. Please restart.")

if __name__ == "__main__":
    main()
