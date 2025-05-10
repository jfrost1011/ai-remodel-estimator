# ui/pages.py
import streamlit as st
from backend import estimator

def render_home():
    st.title("🏠 AI Renovation Cost Estimator")
    st.write("Enter your project details in the sidebar →")
    
    st.markdown("""
    ## Welcome to the Renovation Cost Estimator!
    
    This tool helps you estimate costs for common home renovation projects.
    
    ### How it works:
    1. Select the "Estimator" page from the sidebar
    2. Enter your project details
    3. Get an instant cost estimate based on your inputs
    
    ### Try it now:
    Use the navigation in the sidebar to get started.
    """)

def render_estimator():
    st.title("✏️ Renovation Cost Estimator")
    st.write("Fill out the details in the sidebar to get your estimate")
    
    st.sidebar.header("Project details")

    zip_code = st.sidebar.text_input("ZIP code", "90210")
    project_type = st.sidebar.selectbox("Project type",
                                        ["kitchen", "bathroom", "addition"])
    square_feet = st.sidebar.number_input("Square footage", 50.0, 10000.0, 200.0)
    material_grade = st.sidebar.selectbox("Material grade",
                                          ["economy", "standard", "premium"])
    timeline = st.sidebar.selectbox("Timeline",
                                     ["flexible", "standard", "rush"])

    if st.sidebar.button("Estimate"):
        with st.spinner("Calculating estimate..."):
            result = estimator.simple_estimate(zip_code,
                                           project_type,
                                           square_feet,
                                           material_grade,
                                           timeline)
        
        st.success(f"Estimated total cost: **${result['total']:,}** "
                   f"(${result['per_sqft']}/sq ft)")
        
        # Show a breakdown of the estimate
        st.subheader("Cost Breakdown")
        st.markdown(f"""
        - **Project Type:** {project_type.title()}
        - **Square Footage:** {square_feet} sq ft
        - **Material Grade:** {material_grade.title()}
        - **Timeline:** {timeline.title()}
        - **ZIP Code:** {zip_code}
        """)
        
        # Add a sample chart
        import pandas as pd
        import numpy as np
        
        # Create some sample data for the chart
        categories = ["Labor", "Materials", "Permits", "Other"]
        percentages = [0.45, 0.35, 0.10, 0.10]
        values = [round(result['total'] * p, 2) for p in percentages]
        
        chart_data = pd.DataFrame({
            'Category': categories,
            'Cost': values
        })
        
        st.bar_chart(chart_data, x='Category', y='Cost')

# For compatibility with existing imports
def render_home_page():
    render_home()
    
def render_estimate_page():
    render_estimator()
    
def render_search_page():
    st.title("🔍 Smart Search")
    st.info("This feature is currently under development. Please check back later.")
    
def render_dashboard_page():
    st.title("📊 Dashboard")
    st.info("This feature is currently under development. Please check back later.")
    
def render_admin_page():
    st.title("⚙️ Admin")
    st.info("This feature is currently under development. Please check back later.") 