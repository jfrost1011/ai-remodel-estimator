"""
Market Research Component for the Renovation Estimator UI

This module provides UI components for performing real-time market research
using the Tavily API. It includes components for searching renovation costs
based on location and project type.
"""

import streamlit as st
import time
import sys
import os
from typing import Dict, Any, List, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import backend functionality
try:
    from backend.tavily_search import search_renovation_costs, get_tavily_provider
    TAVILY_AVAILABLE = get_tavily_provider().is_available
except ImportError as e:
    logger.error(f"Error importing Tavily search module: {str(e)}")
    TAVILY_AVAILABLE = False

def render_market_research_section(show_in_sidebar: bool = False):
    """
    Render the market research section in the UI.
    
    Args:
        show_in_sidebar: Whether to show the section in the sidebar
    """
    container = st.sidebar if show_in_sidebar else st
    
    with container.expander("🔍 Market Research (Real-time Cost Data)", expanded=not show_in_sidebar):
        st.write("Get up-to-date renovation cost information for your area.")
        
        if not TAVILY_AVAILABLE:
            st.warning("Real-time market research is currently unavailable. Please check your Tavily API key.")
            
            if st.button("Setup Tavily Integration"):
                st.info("To enable real-time market research, you need a Tavily API key.")
                st.markdown("1. Sign up at [Tavily.com](https://tavily.com/) to get your API key")
                st.markdown("2. Add your API key to the `.env` file: `TAVILY_API_KEY=your-key`")
                st.markdown("3. Install the Tavily package: `pip install tavily-python`")
            return
        
        # Form for market research
        with st.form("market_research_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_type = st.selectbox(
                    "Project Type",
                    options=["kitchen", "bathroom", "addition", "basement", "living room", "bedroom"],
                    index=0
                )
            
            with col2:
                location = st.text_input("Location (City, State or ZIP)", value="San Diego, CA")
            
            advanced_options = st.checkbox("Advanced Options")
            
            if advanced_options:
                col1, col2 = st.columns(2)
                with col1:
                    size = st.number_input("Size (square feet)", min_value=0, value=0)
                    size = size if size > 0 else None
                
                with col2:
                    quality = st.selectbox(
                        "Quality Level",
                        options=["any", "economy", "standard", "premium", "luxury"],
                        index=0
                    )
                    quality = None if quality == "any" else quality
            else:
                size = None
                quality = None
            
            submit_button = st.form_submit_button("Search Market Rates")
        
        # Handle form submission
        if submit_button:
            with st.spinner(f"Searching for {project_type} renovation costs in {location}..."):
                try:
                    results = search_renovation_costs(project_type, location, size, quality)
                    display_market_research_results(results)
                except Exception as e:
                    st.error(f"Error searching for renovation costs: {str(e)}")
                    logger.error(f"Error in market research: {str(e)}")
                    st.error("An error occurred while searching for renovation costs. Please try again later.")

def display_market_research_results(results: Dict[str, Any]):
    """
    Display the market research results in the UI.
    
    Args:
        results: The results from the market research search
    """
    if "error" in results:
        st.error(results["error"])
        return
    
    if not results.get("found_costs", False):
        st.warning("No specific cost information found. Try adjusting your search criteria.")
        return
    
    # Display query and found costs
    st.subheader("Market Research Results")
    st.write(f"**Search Query:** {results.get('query', '')}")
    
    # Create a nicely formatted card for cost information
    st.markdown("### Cost Information")
    
    cost_container = st.container()
    with cost_container:
        st.markdown(
            '<div style="background-color:#f0f2f6;padding:20px;border-radius:10px;margin-bottom:20px">'
            '<h4 style="margin-top:0">Price Ranges Found</h4>'
            '<ul>',
            unsafe_allow_html=True
        )
        
        for cost_range in results.get("cost_ranges", []):
            st.markdown(f'<li style="margin-bottom:8px">{cost_range}</li>', unsafe_allow_html=True)
        
        st.markdown('</ul></div>', unsafe_allow_html=True)
    
    # Display sources
    st.markdown("### Sources")
    
    for i, source in enumerate(results.get("top_sources", []), 1):
        with st.expander(f"{i}. {source.get('title', 'Source')}"):
            st.markdown(f"**Preview:** {source.get('preview', '')}...")
            st.markdown(f"**URL:** [{source.get('url', '')}]({source.get('url', '')})")

def market_research_page():
    """Standalone page for market research."""
    st.title("Renovation Cost Market Research")
    
    st.write("""
    This tool provides real-time market research on renovation costs in different locations.
    It searches the web for the most up-to-date cost information for your specific project.
    """)
    
    # Add a descriptive section
    st.markdown("""
    ### Why Use Market Research?
    - Get current cost information specific to your location
    - Find price ranges for different project types and sizes
    - Access data from multiple reliable sources
    - Make more informed decisions for your renovation project
    """)
    
    # Show the main research component
    render_market_research_section(show_in_sidebar=False)
    
    # Add some contextual information at the bottom
    st.info("""
    **Note:** Cost estimates from market research are based on publicly available information and may vary.
    For the most accurate estimate, consult with local contractors in your area.
    """)

if __name__ == "__main__":
    # This allows the component to be run directly for testing
    market_research_page() 