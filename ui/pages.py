import streamlit as st
from backend import estimator  # backend/estimator.py must exist

# ───────────────────────────────────────────────────────────── #
# Page render functions
# ───────────────────────────────────────────────────────────── #

def render_home():
    st.title("🏠 AI Renovation Cost Estimator")
    st.write("Enter your project details in the sidebar ➡️")

def render_estimator():
    st.sidebar.header("Project details")

    zip_code      = st.sidebar.text_input("ZIP code", "90210")
    project_type  = st.sidebar.selectbox(
        "Project type", ["kitchen", "bathroom", "addition"]
    )
    square_feet   = st.sidebar.number_input(
        "Square footage", min_value=50, max_value=10_000, value=250
    )
    material      = st.sidebar.selectbox(
        "Material grade", ["economy", "standard", "premium"]
    )
    timeline      = st.sidebar.selectbox(
        "Timeline", ["flexible", "standard", "rush"]
    )

    if st.sidebar.button("Estimate"):
        res = estimator.simple_estimate(
            zip_code, project_type, square_feet, material, timeline
        )
        st.success(
            f"Estimated total cost: **${res['total']:,}** "
            f"(${res['per_sqft']}/sq ft)"
        )

# ───────────────────────────────────────────────────────────── #
# Router dictionary (imported in streamlit_app.py)
# ───────────────────────────────────────────────────────────── #
pages = {
    "Home": render_home,
    "Estimator": render_estimator,
} 