import streamlit as st
from backend import estimator

def render_home():
    st.title("🏠 AI Renovation Cost Estimator")
    st.write("Enter your project details in the sidebar →")

def render_estimator():
    st.sidebar.header("Project details")

    zip_code = st.sidebar.text_input("ZIP code", "90210")
    project_type = st.sidebar.selectbox(
        "Project type", ["kitchen", "bathroom", "addition"])
    square_feet = st.sidebar.number_input(
        "Square footage", min_value=50.0, max_value=10000.0, value=200.0)
    material_grade = st.sidebar.selectbox(
        "Material grade", ["economy", "standard", "premium"])
    timeline = st.sidebar.selectbox(
        "Timeline", ["flexible", "standard", "rush"])

    if st.sidebar.button("Estimate"):
        result = estimator.simple_estimate(
            zip_code, project_type, square_feet, material_grade, timeline)
        st.success(
            f"Estimated total cost: **${result['total']:,}** "
            f"(${result['per_sqft']}/sq ft)"
        )

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