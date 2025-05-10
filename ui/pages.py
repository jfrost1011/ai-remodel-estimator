import streamlit as st
from backend import estimator

def render_home():
    st.title("AI Renovation Cost Estimator")
    st.write("Use the sidebar to navigate")

def render_estimator():
    st.sidebar.header("Enter details")
    
    zip_code = st.sidebar.text_input("ZIP code", "90210")
    project_type = st.sidebar.selectbox("Project type", ["kitchen", "bathroom", "addition"])
    square_feet = st.sidebar.number_input("Square footage", 50, 10000, 250)
    material = st.sidebar.selectbox("Material grade", ["economy", "standard", "premium"])
    timeline = st.sidebar.selectbox("Timeline", ["flexible", "standard", "rush"])
    
    if st.sidebar.button("Estimate"):
        result = estimator.simple_estimate(zip_code, project_type, square_feet, material, timeline)
        st.success(f"Total cost: ${result['total']:,} (${result['per_sqft']}/sq ft)")

pages = {
    "Home": render_home,
    "Estimator": render_estimator
}
