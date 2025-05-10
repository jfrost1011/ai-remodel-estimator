"""
Renovation Cost Estimator Application

This is the main application for the Renovation Cost Estimator.
It serves as the entry point for Streamlit and handles navigation and page routing.
"""

import streamlit as st
from dotenv import load_dotenv
import os
from ui.pages import pages

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Remodel Cost Estimator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App styling
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
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
    /* Main app header styling */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    /* Metrics styling */
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    [data-testid="stMetric"] > div {
        display: flex;
        justify-content: center;
        text-align: center;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 500;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 600;
        color: #1e88e5;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        font-weight: 400;
    }
    /* Button styling */
    .stButton > button {
        background-color: #1e88e5;
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #1976d2;
    }
    /* Form submit button */
    button[kind="primaryFormSubmit"] {
        background-color: #1e88e5;
        color: white;
        border: none;
    }
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        background-color: #f8f9fa;
    }
    /* Sidebar title */
    .sidebar-title {
        margin-bottom: 0;
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
    }
    /* Footer info */
    .sidebar-footer {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
    }
    /* PDF warning styling */
    .pdf-warning {
        padding: 10px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
    /* Active navigation item */
    .css-1djdyxw:hover {
        color: #f63366;
    }
    /* Cost range */
    .cost-range {
        font-size: 1.2rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    /* App title container */
    .title-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
    }
    .title-emoji {
        font-size: 2.5rem;
    }
    .title-text {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    /* Download button styling */
    .download-button {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin-right: 10px;
        margin-bottom: 10px;
        background-color: #4CAF50;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
    }
    .download-button.blue {
        background-color: #2196F3;
    }
    .download-button:hover {
        opacity: 0.9;
    }
    /* Warning box styling */
    .warning-box {
        padding: 1rem;
        background-color: #FFF3CD;
        color: #856404;
        border-left: 5px solid #FFD700;
        margin: 1rem 0;
        border-radius: 4px;
    }
    /* Export section styling */
    .export-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 30px;
        border: 1px solid #e9ecef;
    }
    .export-section h3 {
        margin-top: 0;
        color: #2c3e50;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
def main():
    # App header in the sidebar with money bag emoji for estimator
    st.sidebar.markdown('<p class="sidebar-title">🏠 AI Remodel Cost Estimator</p>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio("Navigation", list(pages.keys()))
    st.sidebar.markdown("---")
    
    # Display page title with emoji based on current page
    if page == "Home":
        emoji = "🏠"
    else:
        emoji = "💰"
    
    # Display the title with emoji
    st.markdown(
        f'<div class="title-container">'
        f'<span class="title-emoji">{emoji}</span>'
        f'<span class="title-text">Renovation Cost Estimator</span>'
        f'</div>', 
        unsafe_allow_html=True
    )
    
    # Display the selected page
    pages[page]()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### About")
    st.sidebar.markdown(
        '<div class="sidebar-footer">This app provides cost estimates for common renovation projects.<br><br>'
        '© 2023 HomeAdvisorAI</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
