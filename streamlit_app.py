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

# Import the UI pages
from ui import pages

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

# Define page mapping
PAGES = {
    "Home": pages.render_home,
    "Estimator": pages.render_estimator,
    "Search": pages.render_search_page,
    "Dashboard": pages.render_dashboard_page,
    "Admin": pages.render_admin_page
}

# Create the sidebar
st.sidebar.title("🏠 Renovation Estimator")
st.sidebar.markdown("---")

# Navigation
choice = st.sidebar.radio("Navigation", list(PAGES.keys()))

# Credits
st.sidebar.markdown("---")
st.sidebar.caption("© 2024 Renovation Estimator")

# Render the selected page
PAGES[choice]()
