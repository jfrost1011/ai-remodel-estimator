"""
Renovation Cost Estimator Application

This is the main application for the Renovation Cost Estimator.
It serves as the entry point for Streamlit and handles navigation and page routing.
"""

import streamlit as st
from dotenv import load_dotenv
from ui.pages import pages

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Renovation Cost Estimator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6f0ff;
        border-bottom: 2px solid #4b78e6;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
def main():
    page = st.sidebar.radio("Navigation", list(pages.keys()))
    st.sidebar.markdown("---")
    
    # Display the selected page
    pages[page]()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### About")
    st.sidebar.info(
        """
        This app provides cost estimates for common renovation projects.
        
        © 2023 HomeAdvisorAI
        """
    )

if __name__ == "__main__":
    main()
