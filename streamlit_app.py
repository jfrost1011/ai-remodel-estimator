"""
Streamlit Cloud Entry Point for Renovation Cost Estimator

This file serves as the designated entry point for Streamlit Cloud deployment.
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
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")  # Prevents warnings

# Import UI components
import streamlit as st
from dotenv import load_dotenv

# Try to load any .env file if it exists
load_dotenv()

# Configure the app
st.set_page_config(
    page_title="Renovation Cost Estimator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the app modules dynamically
import importlib.util
spec = importlib.util.spec_from_file_location("app", str(renovation_dir / "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Import necessary UI components
sys.path.append(str(renovation_dir / "ui"))
from ui.home_page import render_home_page
from ui.estimate_page import render_estimate_page
from ui.search_page import render_search_page
from ui.dashboard_page import render_dashboard_page
from ui.admin_page import render_admin_page

# Define the render_sidebar function (copied from app.py but accessible here)
def render_sidebar():
    """Render the application sidebar with navigation options."""
    with st.sidebar:
        st.title("🏠 Renovation Estimator")
        
        # Navigation
        selected_page = st.radio(
            "Navigation",
            ["Home", "Cost Estimator", "Smart Search", "Dashboard", "Admin"],
            index=0
        )
        
        # App info
        st.sidebar.markdown("---")
        st.sidebar.info(
            "This application provides accurate cost estimates for home renovation projects using AI and real market data."
        )
        
        # App version and integration info
        st.sidebar.markdown("---")
        st.sidebar.caption("App Version: 1.1.0")
        
        # Display embedding model info
        embedding_model = os.environ.get("EMBEDDING_MODEL_PATH", "jfrost10/renovation-cost-estimator-fine-tune")
        pinecone_status = "Enabled" if os.environ.get("USE_PINECONE", "false").lower() == "true" else "Disabled"
        mock_data = "Yes" if os.environ.get("MOCK_DATA", "true").lower() == "true" else "No"
        
        with st.sidebar.expander("Integration Status"):
            st.caption(f"**Embedding Model:** {embedding_model}")
            st.caption(f"**Pinecone Integration:** {pinecone_status}")
            st.caption(f"**Using Mock Data:** {mock_data}")
            
            # Check if embeddings model is loaded
            try:
                from utils.langchain_vector_store import get_langchain_embeddings
                embeddings = get_langchain_embeddings()
                if embeddings:
                    st.caption("✅ Embedding model loaded successfully")
                else:
                    st.caption("❌ Embedding model failed to load")
            except Exception as e:
                st.caption("❌ Could not verify embedding model status")
                st.caption(f"Error: {e}")
        
        # Credits
        st.sidebar.markdown("---")
        st.sidebar.caption("© 2024 Renovation Estimator")
        
        return selected_page

def main():
    """Main application function that handles page rendering."""
    try:
        # Save selected page in session state for navigation between pages
        if "sidebar_selection" not in st.session_state:
            st.session_state["sidebar_selection"] = None
        
        # Render sidebar and get selected page
        selected_page = render_sidebar()
        
        # Override selected page if set in session state
        if st.session_state.get("sidebar_selection"):
            selected_page = st.session_state["sidebar_selection"]
            # Reset after use
            st.session_state["sidebar_selection"] = None
        
        # Render selected page within try/except to catch errors
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
            st.error(f"Error loading page: {e}")
            st.info("Try restarting the application or contact support if the issue persists.")
    except Exception as e:
        st.error(f"The application encountered a critical error: {e}")
        st.error("Please restart or contact support.")

if __name__ == "__main__":
    main() 